import os

from verify4py.UniversityDiplomaIssuer import UniversityDiplomaIssuer


def test_issued_pdf_with_signature():
    issuer = UniversityDiplomaIssuer('0xc0668aC1BE4393F9dA6c8eB81a24faA4F9B04Edb',
                                     'https://node-testnet.teo.mn',
                                     '0x259164d9D26a1bcC8aE3B721aC23F0e2A5563D07',
                                     issuer_name='Test')
    pk = os.environ['PRIVATE_KEY']
    tx, error = issuer.issued_pdf_with_signature('tt', '/home/surenbayar/Downloads/test.pdf',
                                                 '/home/surenbayar/Downloads/test_issued.pdf', {
                                                     "CONFER_YEAR_NAME": "2022-2023 хичээлийн жил",
                                                     "DEGREE_NUMBER": "tt",
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
                                                 '0x9b7b3268d9860bc6b3e760574d8d451e0b1b10f483a356ae379212bce48991b30af940b82e5b7cbba5a1ab05db860065e8db13d3e08f18e62172e0bc828c4b4f1c',
                                                 pk)
    assert error == '' or error is None
