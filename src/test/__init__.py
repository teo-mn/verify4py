from verify4py.UniversityDiplomaIssuer import UniversityDiplomaIssuer

if __name__ == "__main__":
    issuer = UniversityDiplomaIssuer('0xc0668aC1BE4393F9dA6c8eB81a24faA4F9B04Edb', 'https://node-testnet'
                                                                                   '.corexchain.io',
                                     '0x259164d9D26a1bcC8aE3B721aC23F0e2A5563D07', 'test3', 3305)
    meta_data = {
            "DEGREE_NUMBER": "D202201963",
            "PRIMARY_IDENTIFIER_NUMBER": "дй99051406",
            "INSTITUTION_ID": 35580,
            "INSTITUTION_NAME": "МУБИС /Монгол улсын боловсролын их сургууль/",
            "EDUCATION_LEVEL_NAME": "Бакалаврын боловсрол",
            "EDUCATION_FIELD_CODE": "011412",
            "EDUCATION_FIELD_NAME": "Багш, эрүүл мэндийн боловсрол",
            "TOTAL_GPA": 3.3,
            "LAST_NAME": "Батжаргал",
            "FIRST_NAME": "Сугармаа",
            "CONFER_YEAR_NAME": "2021-2022 хичээлийн жил"
        }
    try:
        x = issuer.issue_pdf(meta_data['DEGREE_NUMBER'], '/home/surenbayar/test.pdf',
                             '/home/surenbayar/test_verified.pdf',
                             meta_data, 0, '', '',
                             '65245c75a01178dae360ba4e1df32f8a0058cf92ba8b325c3ce0be4eb340c945')
        print(x)
    except Exception as e:
        print(e)
