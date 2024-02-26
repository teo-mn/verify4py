import os

from verify4py.UniversityDiplomaIssuer import UniversityDiplomaIssuer


def test_issued_pdf_with_signature():
    issuer = UniversityDiplomaIssuer('0xc0668aC1BE4393F9dA6c8eB81a24faA4F9B04Edb',
                                     'https://node-testnet.teo.mn',
                                     '0x259164d9D26a1bcC8aE3B721aC23F0e2A5563D07',
                                     issuer_name='Test')
    tx, error = issuer.issued_pdf_with_signature('test', '/home/surenbayar/Downloads/test.pdf',
                                     '/home/surenbayar/Downloads/test_issued.pdf', {}, 0,
                                     'test', '', '',
                                     os.environ['PRIVATE_KEY'])
    assert error == '' or error is None
