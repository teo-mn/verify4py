import os

from verify4py.UniversityDiplomaIssuer import UniversityDiplomaIssuer


def test_issued_pdf_with_signature():
    issuer = UniversityDiplomaIssuer('0xc0668aC1BE4393F9dA6c8eB81a24faA4F9B04Edb',
                                     'https://node-testnet.teo.mn',
                                     '0x259164d9D26a1bcC8aE3B721aC23F0e2A5563D07',
                                     issuer_name='Test')
    pk = os.environ['PRIVATE_KEY']
    tx, error = issuer.issued_pdf_with_signature('xx', '/home/surenbayar/Downloads/test.pdf',
                                                 '/home/surenbayar/Downloads/test_issued.pdf', {
                                                     "CONFER_YEAR_NAME": "2022-2023 хичээлийн жил",
                                                     "DEGREE_NUMBER": "xx",
                                                     "EDUCATION_FIELD_CODE": "051202",
                                                     "EDUCATION_FIELD_NAME": "Тест",
                                                     "EDUCATION_LEVEL_NAME": "бакалаврын боловсрол",
                                                     "FIRST_NAME": "Тест",
                                                     "INSTITUTION_ID": 1,
                                                     "INSTITUTION_NAME": "Тест Их Сургууль",
                                                     "LAST_NAME": "Тест",
                                                     "PRIMARY_IDENTIFIER_NUMBER": "aa99887766",
                                                     "TOTAL_GPA": 4
                                                 }, 0,
                                                 'test', '',
                                                 '0x7efbf6cf80130d69156d60d8e92cb13b351b4532b01a690e8d7de0c3f7cc96c958e76e18771efd5ac698f14375aabaa3f765b1e28e8f2184eabc75aebeb740e21c',
                                                 pk)
    assert error == '' or error is None
