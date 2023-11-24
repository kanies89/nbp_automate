from variables import geo3_country_loc, geo3_country
import pandas as pd


def format_decimal(number):
    formatted_number = "{:.2f}".format(float(number))
    return formatted_number


def create_ar1(tab):
    path = 'Example\\'
    df = pd.read_excel(path + '2023_09_31___BSP_AR1_ST.w.8.7.5.xlsx', sheet_name=tab, header=None,
                       keep_default_na=False)

    year = '2023'
    month = '09'
    day = '30'

    if tab == 'p-dane':
        xml_add_code = ''
        codes1 = df.loc[8, 13:]
        codes2 = df.loc[9:, 0]

        xml = """<?xml version='1.0' encoding='UTF-8'?>
<xbrli:xbrl xmlns:xbrli="http://www.xbrl.org/2003/instance" xmlns:d-BSP-uz="http://bsp.nbp.pl/BazaSystemuPlatniczego/1.1.1/d-BSP-uz-2022-01-01" xmlns:d-BSP-ts="http://bsp.nbp.pl/BazaSystemuPlatniczego/1.1.1/d-BSP-ts-2022-01-01" xmlns:d-dane="http://bsp.nbp.pl/1.1.1/d-dane-2017-08-09" xmlns:d-BSP-tw="http://bsp.nbp.pl/BazaSystemuPlatniczego/1.1.1/d-BSP-tw-2022-01-01" xmlns:p-dane="http://bsp.nbp.pl/1.1.1/p-dane-2017-08-09" xmlns:d-BSP-ps="http://bsp.nbp.pl/BazaSystemuPlatniczego/1.1.1/d-BSP-ps-2022-01-01" xmlns:iso4217="http://www.xbrl.org/2003/iso4217" xmlns:d-BSP-kw="http://bsp.nbp.pl/BazaSystemuPlatniczego/1.1.1/d-BSP-kw-2022-01-01" xmlns:p-BSP-measures="http://bsp.nbp.pl/BazaSystemuPlatniczego/1.1.1/p-BSP-measures-2022-01-01" xmlns:d-BSP-ur="http://bsp.nbp.pl/BazaSystemuPlatniczego/1.1.1/d-BSP-ur-2022-01-01" xmlns:d-BSP-kt="http://bsp.nbp.pl/BazaSystemuPlatniczego/1.1.1/d-BSP-kt-2022-01-01" xmlns:d-BSP-ro="http://bsp.nbp.pl/BazaSystemuPlatniczego/1.1.1/d-BSP-ro-2022-01-01" xmlns:xbrldi="http://xbrl.org/2006/xbrldi" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:link="http://www.xbrl.org/2003/linkbase">
<link:schemaRef xlink:type="simple" xlink:arcrole="http://www.w3.org/1999/xlink/properties/linkbase" xlink:href="t-BSP-2022-01-01.xsd"/>
<xbrli:unit id="PURE">
    <xbrli:measure>xbrli:pure</xbrli:measure>
</xbrli:unit>
<xbrli:unit id="PLN">
    <xbrli:measure>iso4217:PLN</xbrli:measure>
</xbrli:unit>
"""
        xml_add_code += xml

        for number1, code1 in enumerate(codes1):
            for number2, code2 in enumerate(codes2):
                code = code1 + code2
                taxonomy = code.split('_')

                value = df.iat[9 + number2, 13 + number1]
                print(taxonomy, tab)
                xml = f"""
<xbrli:context id="{tab}_{number1}{number2}">
    <xbrli:entity>
      <xbrli:identifier scheme=" http://sis.nbp.pl/nbp">60300</xbrli:identifier>
      <xbrli:segment>
        <xbrldi:explicitMember dimension="d-dane:FormularzeWymiar">d-dane:{taxonomy[0]}</xbrldi:explicitMember>
      </xbrli:segment>
    </xbrli:entity>
    <xbrli:period>
      <xbrli:instant>{year}-{month}-{day}</xbrli:instant>
    </xbrli:period>
</xbrli:context>
<p-dane:{taxonomy[1]} id="ft_{tab}_{number1}{number2}" contextRef="{tab}_{number1}{number2}">{value}</p-dane:{taxonomy[1]}>
"""
                xml_add_code += xml

    elif tab == 'ST.01':
        xml_add_code = ''
        codes1 = df.loc[9:, 0]
        codes2 = df.loc[5, 13:]

        for number1, code1 in enumerate(codes1):
            for number2, code2 in enumerate(codes2):
                code = code1 + code2
                taxonomy = code.split('_')
                print(taxonomy, tab, number1, number2)
                value = df.iat[9 + number1, 13 + number2]

                if taxonomy[0] in ['M11', 'M13', 'M14', 'M202']:
                    if value == '':
                        value = 0
                    unit = [
                        'PLN',
                        '2',
                        format_decimal(value)
                    ]
                else:
                    if value == '':
                        value = '0'
                    unit = [
                        'PURE',
                        '0',
                        value
                    ]

                xml = f"""
<xbrli:context id="{tab}_{number1}{number2}">
<xbrli:entity>
  <xbrli:identifier scheme=" http://sis.nbp.pl/nbp">60300</xbrli:identifier>
  <xbrli:segment>
    <xbrldi:explicitMember dimension="d-BSP-ur:RodzajUrzadzeniaWymiar">d-BSP-ur:{taxonomy[1]}</xbrldi:explicitMember>
    <xbrldi:explicitMember dimension="d-BSP-tw:TerytoriumWydawcyWymiar">d-BSP-tw:{taxonomy[2]}</xbrldi:explicitMember>
  </xbrli:segment>
</xbrli:entity>
<xbrli:period>
  <xbrli:instant>{year}-{month}-{day}</xbrli:instant>
</xbrli:period>
</xbrli:context>
<p-BSP-measures:{taxonomy[0]} id="ft_{tab}_{number1}{number2}" contextRef="{tab}_{number1}{number2}" unitRef="{unit[0]}" decimals="{unit[1]}">{unit[2]}</p-BSP-measures:{taxonomy[0]}>
"""
                xml_add_code += xml

    elif tab in ['ST.02', 'ST.03']:
        xml_add_code = ''
        codes1 = df.loc[9:, 0]
        codes2 = df.loc[5, 13:]

        for number1, code1 in enumerate(codes1):
            for number2, code2 in enumerate(codes2):
                code = code1 + code2
                taxonomy = code.split('_')
                print(taxonomy, tab)
                value = df.iat[9 + number1, 13 + number2]

                if taxonomy[0] in ['M11', 'M13', 'M14', 'M202']:
                    if value == '':
                        value = 0
                    unit = [
                        'PURE',
                        '2',
                        format_decimal(value)
                    ]
                else:
                    if value == '':
                        value = '0'
                    unit = [
                        'PURE',
                        '0',
                        value
                    ]

                if len(taxonomy) == 2:
                    xml = f"""
<xbrli:context id="{tab}_{number1}{number2}">
<xbrli:entity>
  <xbrli:identifier scheme=" http://sis.nbp.pl/nbp">60300</xbrli:identifier>
  <xbrli:segment>
    <xbrldi:explicitMember dimension="d-BSP-tw:TerytoriumWydawcyWymiar">d-BSP-tw:{taxonomy[1]}</xbrldi:explicitMember>
  </xbrli:segment>
</xbrli:entity>
<xbrli:period>
  <xbrli:instant>{year}-{month}-{day}</xbrli:instant>
</xbrli:period>
</xbrli:context>
<p-BSP-measures:{taxonomy[0]} id="ft_{tab}_{number1}{number2}" contextRef="{tab}_{number1}{number2}" unitRef="{unit[0]}" decimals="{unit[1]}">{unit[2]}</p-BSP-measures:{taxonomy[0]}>
"""
                else:
                    xml = f"""
<xbrli:context id="{tab}_{number1}{number2}">
<xbrli:entity>
  <xbrli:identifier scheme=" http://sis.nbp.pl/nbp">60300</xbrli:identifier>
  <xbrli:segment>
    <xbrldi:explicitMember dimension="d-BSP-ur:RodzajUrzadzeniaWymiar">d-BSP-ur:{taxonomy[1]}</xbrldi:explicitMember>
    <xbrldi:explicitMember dimension="d-BSP-tw:TerytoriumWydawcyWymiar">d-BSP-tw:{taxonomy[2]}</xbrldi:explicitMember>
  </xbrli:segment>
</xbrli:entity>
<xbrli:period>
  <xbrli:instant>{year}-{month}-{day}</xbrli:instant>
</xbrli:period>
</xbrli:context>
<p-BSP-measures:{taxonomy[0]} id="ft_{tab}_{number1}{number2}" contextRef="{tab}_{number1}{number2}" unitRef="{unit[0]}" decimals="{unit[1]}">{unit[2]}</p-BSP-measures:{taxonomy[0]}>
"""
                xml_add_code += xml

    elif tab in ['ST.04', 'ST.06']:
        xml_add_code = ''
        codes1 = df.loc[9:, 0]
        codes2 = df.loc[5, 13:]

        for number1, code1 in enumerate(codes1):
            for number2, code2 in enumerate(codes2):
                code = code2 + code1
                taxonomy = code.split('_')
                print(taxonomy, tab)
                value = df.iat[9 + number1, 13 + number2]

                if taxonomy[0] in ['M11', 'M13', 'M14', 'M202']:
                    if value == '':
                        value = 0
                    unit = [
                        'PURE',
                        '2',
                        format_decimal(value)
                    ]
                else:
                    if value == '':
                        value = '0'
                    unit = [
                        'PURE',
                        '0',
                        value
                    ]

                if tab == 'ST.04':
                    xml = f"""
<xbrli:context id="{tab}_{number1}{number2}">
<xbrli:entity>
  <xbrli:identifier scheme=" http://sis.nbp.pl/nbp">60300</xbrli:identifier>
  <xbrli:segment>
    <xbrldi:explicitMember dimension="d-BSP-ur:RodzajUrzadzeniaWymiar">d-BSP-ur:{taxonomy[1]}</xbrldi:explicitMember>
    <xbrldi:explicitMember dimension="d-BSP-tw:TerytoriumWydawcyWymiar">d-BSP-tw:{taxonomy[2]}</xbrldi:explicitMember>
    <xbrldi:explicitMember dimension="d-BSP-kw:KrajWydawcyKartyWymiar001">d-BSP-kw:{taxonomy[3]}</xbrldi:explicitMember>
  </xbrli:segment>
</xbrli:entity>
<xbrli:period>
  <xbrli:instant>{year}-{month}-{day}</xbrli:instant>
</xbrli:period>
</xbrli:context>
<p-BSP-measures:{taxonomy[0]} id="ft_{tab}_{number1}{number2}" contextRef="{tab}_{number1}{number2}" unitRef="{unit[0]}" decimals="{unit[1]}">{unit[2]}</p-BSP-measures:{taxonomy[0]}>
"""
                if tab == 'ST.06':
                    if taxonomy[3] not in ['AT', 'BE', 'BG', 'CY', 'HR', 'CZ', 'DK', 'EE', 'FI', 'FR', 'GR', 'ES', 'NL',
                                           'IE', 'IS', 'LI', 'LT', 'LU', 'LV', 'MT', 'DE', 'NO', 'PT', 'RO', 'SK', 'SI',
                                           'SE', 'HU', 'IT', 'GB'
                                           ]:
                        if taxonomy[3] == "WLD":
                            taxonomy[3] = "D09-Pozostale kraje"
                        else:
                            cc = df.iat[9 + number1, 11]
                            taxonomy[3] = taxonomy[3] + '-' + cc
                        xml = f"""
<xbrli:context id="{tab}_{number1}{number2}">
<xbrli:entity>
  <xbrli:identifier scheme=" http://sis.nbp.pl/nbp">60300</xbrli:identifier>
  <xbrli:segment>
    <xbrldi:explicitMember dimension="d-BSP-tw:TerytoriumWydawcyWymiar">d-BSP-tw:{taxonomy[2]}</xbrldi:explicitMember>
    <xbrldi:explicitMember dimension="d-BSP-ro:RodzajeOperacjiWymiar">d-BSP-ro:{taxonomy[1]}</xbrldi:explicitMember>
    <xbrldi:typedMember dimension="d-BSP-kt:KrajWpisywanyWymiar">
      <d-BSP-kt:FNKW01T>{taxonomy[3]}</d-BSP-kt:FNKW01T>
    </xbrldi:typedMember>
  </xbrli:segment>
</xbrli:entity>
<xbrli:period>
  <xbrli:instant>{year}-{month}-{day}</xbrli:instant>
</xbrli:period>
</xbrli:context>
<p-BSP-measures:{taxonomy[0]} id="ft_{tab}_{number1}{number2}" contextRef="{tab}_{number1}{number2}" unitRef="{unit[0]}" decimals="{unit[1]}">{unit[2]}</p-BSP-measures:{taxonomy[0]}>
"""
                    else:
                        xml = f"""
<xbrli:context id="{tab}_{number1}{number2}">
<xbrli:entity>
  <xbrli:identifier scheme=" http://sis.nbp.pl/nbp">60300</xbrli:identifier>
  <xbrli:segment>
    <xbrldi:explicitMember dimension="d-BSP-tw:TerytoriumWydawcyWymiar">d-BSP-tw:{taxonomy[2]}</xbrldi:explicitMember>
    <xbrldi:explicitMember dimension="d-BSP-ro:RodzajeOperacjiWymiar">d-BSP-ro:{taxonomy[1]}</xbrldi:explicitMember>
    <xbrldi:explicitMember dimension="d-BSP-kw:KrajWydawcyKartyWymiar001">d-BSP-kw:{taxonomy[3]}</xbrldi:explicitMember>
  </xbrli:segment>
</xbrli:entity>
<xbrli:period>
  <xbrli:instant>{year}-{month}-{day}</xbrli:instant>
</xbrli:period>
</xbrli:context>
<p-BSP-measures:{taxonomy[0]} id="ft_{tab}_{number1}{number2}" contextRef="{tab}_{number1}{number2}" unitRef="{unit[0]}" decimals="{unit[1]}">{unit[2]}</p-BSP-measures:{taxonomy[0]}>
"""
                xml_add_code += xml

    elif tab in ['ST.05', 'ST.07']:
        xml_add_code = ''
        codes1 = df.loc[9:, 0]
        codes2 = df.loc[5, 13:]

        for number1, code1 in enumerate(codes1):
            for number2, code2 in enumerate(codes2):
                code = code2.split("_")[0] + code1 + code2.split("_")[1]
                taxonomy = code.split('_')
                print(taxonomy, tab)
                value = df.iat[9 + number1, 13 + number2]

                if taxonomy[0] in ['M11', 'M13', 'M14', 'M202']:
                    if value == '':
                        value = 0
                    unit = [
                        'PLN',
                        '2',
                        format_decimal(value)
                    ]
                else:
                    if value == '':
                        value = '0'
                    unit = [
                        'PURE',
                        '0',
                        value
                    ]
                if tab == 'ST.07':
                    if taxonomy[2] in ['SAG', 'SAK']:
                        xml = f"""
<xbrli:context id="{tab}_{number1}{number2}">
<xbrli:entity>
  <xbrli:identifier scheme=" http://sis.nbp.pl/nbp">60300</xbrli:identifier>
  <xbrli:segment>
    <xbrldi:explicitMember dimension="d-BSP-ps:PonoszacyStratyWymiar">d-BSP-ps:{taxonomy[2]}</xbrldi:explicitMember>
    <xbrldi:explicitMember dimension="d-BSP-ro:RodzajeOperacjiWymiar">d-BSP-ro:{taxonomy[1]}</xbrldi:explicitMember>
  </xbrli:segment>
</xbrli:entity>
<xbrli:period>
  <xbrli:instant>{year}-{month}-{day}</xbrli:instant>
</xbrli:period>
</xbrli:context>
<p-BSP-measures:{taxonomy[0]} id="ft_{tab}_{number1}{number2}" contextRef="{tab}_{number1}{number2}" unitRef="{unit[0]}" decimals="{unit[1]}">{unit[2]}</p-BSP-measures:{taxonomy[0]}>
"""
                    else:
                        xml = f"""
<xbrli:context id="{tab}_{number1}{number2}">
<xbrli:entity>
  <xbrli:identifier scheme=" http://sis.nbp.pl/nbp">60300</xbrli:identifier>
  <xbrli:segment>
    <xbrldi:explicitMember dimension="d-BSP-tw:TerytoriumWydawcyWymiar">d-BSP-tw:{taxonomy[2]}</xbrldi:explicitMember>
    <xbrldi:explicitMember dimension="d-BSP-ro:RodzajeOperacjiWymiar">d-BSP-ro:{taxonomy[1]}</xbrldi:explicitMember>
  </xbrli:segment>
</xbrli:entity>
<xbrli:period>
  <xbrli:instant>{year}-{month}-{day}</xbrli:instant>
</xbrli:period>
</xbrli:context>
<p-BSP-measures:{taxonomy[0]} id="ft_{tab}_{number1}{number2}" contextRef="{tab}_{number1}{number2}" unitRef="{unit[0]}" decimals="{unit[1]}">{unit[2]}</p-BSP-measures:{taxonomy[0]}>
"""
                elif tab == 'ST.05':
                    if len(taxonomy) == 3:
                        xml = f"""
<xbrli:context id="{tab}_{number1}{number2}">
<xbrli:entity>
  <xbrli:identifier scheme=" http://sis.nbp.pl/nbp">60300</xbrli:identifier>
  <xbrli:segment>
    <xbrldi:explicitMember dimension="d-BSP-tw:TerytoriumWydawcyWymiar">d-BSP-tw:{taxonomy[2]}</xbrldi:explicitMember>
    <xbrldi:explicitMember dimension="d-BSP-ro:RodzajeOperacjiWymiar">d-BSP-ro:{taxonomy[1]}</xbrldi:explicitMember>
  </xbrli:segment>
</xbrli:entity>
<xbrli:period>
  <xbrli:instant>{year}-{month}-{day}</xbrli:instant>
</xbrli:period>
</xbrli:context>
<p-BSP-measures:{taxonomy[0]} id="ft_{tab}_{number1}{number2}" contextRef="{tab}_{number1}{number2}" unitRef="{unit[0]}" decimals="{unit[1]}">{unit[2]}</p-BSP-measures:{taxonomy[0]}>
"""

                    elif len(taxonomy) == 4:
                        xml = f"""
<xbrli:context id="{tab}_{number1}{number2}">
<xbrli:entity>
  <xbrli:identifier scheme=" http://sis.nbp.pl/nbp">60300</xbrli:identifier>
  <xbrli:segment>
    <xbrldi:explicitMember dimension="d-BSP-tw:TerytoriumWydawcyWymiar">d-BSP-tw:{taxonomy[3]}</xbrldi:explicitMember>
    <xbrldi:explicitMember dimension="d-BSP-ro:RodzajeOperacjiWymiar">d-BSP-ro:{taxonomy[2]}</xbrldi:explicitMember>
    <xbrldi:explicitMember dimension="d-BSP-uz:UzytkownikWymiar">d-BSP-uz:{taxonomy[1]}</xbrldi:explicitMember>
  </xbrli:segment>
</xbrli:entity>
<xbrli:period>
  <xbrli:instant>2023-03-31</xbrli:instant>
</xbrli:period>
</xbrli:context>
<p-BSP-measures:{taxonomy[0]} id="ft_{tab}_{number1}{number2}" contextRef="{tab}_{number1}{number2}" unitRef="{unit[0]}" decimals="{unit[1]}">{unit[2]}</p-BSP-measures:{taxonomy[0]}>
"""

                    elif len(taxonomy) == 5:
                        xml = f"""
<xbrli:context id="{tab}_{number1}{number2}">
<xbrli:entity>
  <xbrli:identifier scheme=" http://sis.nbp.pl/nbp">60300</xbrli:identifier>
  <xbrli:segment>
    <xbrldi:explicitMember dimension="d-BSP-tw:TerytoriumWydawcyWymiar">d-BSP-tw:{taxonomy[4]}</xbrldi:explicitMember>
    <xbrldi:explicitMember dimension="d-BSP-ts:TransakcjeWymiar">d-BSP-ts:{taxonomy[1]}</xbrldi:explicitMember>
    <xbrldi:explicitMember dimension="d-BSP-ro:RodzajeOperacjiWymiar">d-BSP-ro:{taxonomy[3]}</xbrldi:explicitMember>
    <xbrldi:explicitMember dimension="d-BSP-uz:UzytkownikWymiar">d-BSP-uz:{taxonomy[2]}</xbrldi:explicitMember>
  </xbrli:segment>
</xbrli:entity>
<xbrli:period>
  <xbrli:instant>2023-03-31</xbrli:instant>
</xbrli:period>
</xbrli:context>
<p-BSP-measures:{taxonomy[0]} id="ft_{tab}_{number1}{number2}" contextRef="{tab}_{number1}{number2}" unitRef="{unit[0]}" decimals="{unit[1]}">{unit[2]}</p-BSP-measures:{taxonomy[0]}>
"""
                xml_add_code += xml

    return xml_add_code


if __name__ == '__main__':
    xml_code = ''

    EXCEL_READ_AR1 = [
        'p-dane',
        'ST.01',
        'ST.02',
        'ST.03',
        'ST.04',
        'ST.05',
        'ST.06',
        'ST.07'
    ]
    for sheet in EXCEL_READ_AR1:
        xml_code += create_ar1(sheet)

    xml_code += '</xbrli:xbrl>'

    with open("PayTel_fjk_20230930_AR1.txt", 'w', encoding="utf-8") as file:
        file.write(xml_code)
