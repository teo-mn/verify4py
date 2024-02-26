import json
import os

from pdfrw import PdfReader

import verify4py.pdf as pdf_utils
import verify4py.utils as Utils
from verify4py.Issuer import Issuer
from verify4py.certify_sc_utils import DEFAULT_GAS_LIMIT
from verify4py.json_utils import json_wrap

VERSION = 'v1.0-python-university'


class UniversityDiplomaIssuer(Issuer):
    def __init__(self, smart_contract_address,
                 node_host,
                 issuer_address='',
                 issuer_name='',
                 chain_id=1104,
                 hash_type='sha256'):
        super(UniversityDiplomaIssuer, self).__init__(smart_contract_address,
                                                      node_host, issuer_address,
                                                      issuer_name,
                                                      chain_id,
                                                      hash_type,
                                                      contract_type='university')

    def prepare_issue(self,
                      id: str,
                      source_file_path: str,
                      destination_file_path: str,
                      meta_data: object,
                      desc: str,
                      additional_info: str):
        verifymn = {
            "issuer": {
                "name": self.issuer_name,
                "address": self.issuer_address
            },
            "info": {
                "name": self.issuer_name,
                "desc": desc,
                "cerNum": id,
                "additionalInfo": additional_info
            },
            "version": VERSION,
            "blockchain": {
                "network": "CorexMain" if self.chain_id == 1104 else "CorexTest",
                "smartContractAddress": self.smart_contract_address
            }
        }

        # validation
        if not os.path.exists(source_file_path) or not os.path.isfile(source_file_path):
            raise ValueError('Source path should be valid')

        if os.path.isdir(destination_file_path):
            raise ValueError('Destination path already exists')

        pdf_utils.add_metadata(source_file_path, destination_file_path, verifymn=json.dumps(verifymn))
        hash_image = Utils.calc_hash(destination_file_path)
        verifymn['univ_meta'] = meta_data
        pdf_utils.add_metadata(source_file_path, destination_file_path, verifymn=json.dumps(verifymn))
        hash_val = Utils.calc_hash(destination_file_path)
        meta_str = json_wrap(meta_data)
        hash_meta = Utils.calc_hash_str(meta_str)
        return hash_val, hash_meta, hash_image

    def issue_pdf(self,
                  id: str,
                  source_file_path: str,
                  destination_file_path: str,
                  meta_data: object,
                  expire_date: int,
                  desc: str,
                  additional_info: str,
                  private_key: str = "",
                  key_store="",
                  passphrase: str = ""):

        hash_val, hash_meta, hash_image = self.prepare_issue(id, source_file_path, destination_file_path,
                                                             meta_data, desc, additional_info)
        (tx, proof), error = self.issue(id, hash_val, expire_date, desc, private_key, key_store, passphrase,
                                        hash_image=hash_image, hash_json=hash_meta)
        return tx, error

    def issued_pdf_with_signature(self,
                                  id: str,
                                  source_file_path: str,
                                  destination_file_path: str,
                                  meta_data: object,
                                  expire_date: int,
                                  desc: str,
                                  additional_info: str,
                                  signature: str,
                                  private_key: str = "",
                                  key_store="",
                                  passphrase: str = ""):
        hash_val, hash_meta, hash_image = self.prepare_issue(id, source_file_path, destination_file_path,
                                                             meta_data, desc, additional_info)
        pk = self.get_pk(private_key, key_store, passphrase)

        # check credit
        if self.get_credit(self.issuer_address) == 0:
            raise ValueError("Not enough credit")

        cert = self.get_certificate(hash_val)

        if cert.id > 0 and not cert.isRevoked:  # id
            raise ValueError("Certificate already registered")

        if self.is_duplicated_cert_num(cert_num=id):
            raise ValueError("Certificate number already registered")

        nonce = self.get_client().eth.get_transaction_count(self.get_client().to_checksum_address(self.issuer_address))
        func = self.get_contract_instance().functions.addApprovedCertification(hash_val, hash_image, hash_meta,
                                                                               id, expire_date, desc,
                                                                               self.get_client().to_bytes(
                                                                                   text=signature))
        tx = func.build_transaction(
            {'from': self.issuer_address, 'gasPrice': self.get_client().to_wei('1000', 'gwei'),
             'nonce': nonce, 'gas': DEFAULT_GAS_LIMIT})
        signed = self.get_client().eth.account.sign_transaction(tx, pk)
        tx_hash = self.get_client().eth.send_raw_transaction(signed.rawTransaction)
        tx_res = self.get_client().eth.wait_for_transaction_receipt(tx_hash)
        if tx_res.status == 1:
            try:
                self.write_txid(hash_val, self.get_client().to_hex(tx_hash), self.issuer_address, pk)
            except Exception as e:
                print("Error occurred when sending txid" + str(e))
            return self.get_client().to_hex(tx_hash), None
        print(tx_res)
        return '', 'Failed on blockchain'

    def revoke_pdf(self,
                   file_path: str,
                   revoker_name: str,
                   private_key: str = "",
                   key_store="",
                   passphrase: str = ""
                   ):
        # validation
        if not os.path.exists(file_path) or not os.path.isfile(file_path):
            raise ValueError('Source path should be valid')
        hash_val = Utils.calc_hash(file_path)
        return self.revoke(hash_val.lower(), revoker_name, private_key, key_store, passphrase)

    def verify_pdf(self, file_path):
        hash_val = Utils.calc_hash(file_path)
        pdf = PdfReader(file_path)
        metadata = pdf.Info.get('/verifymn')
        result = self.verify_root(hash_val.lower())
        result['metadata'] = metadata
        return result
