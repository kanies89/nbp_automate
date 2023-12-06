from variables import geo3_country_loc, geo3_country, code_4a_RL, code_4a_RW
import pandas as pd


def format_decimal(number):
    formatted_number = "{:.2f}".format(float(number))
    return formatted_number


def create_ar2(values):
    year = '2023'
    month = '09'
    day = '30'
    code_ar2 = f"""<?xml version="1.0" encoding="UTF-8"?>
<xbrli:xbrl xmlns:xbrli="http://www.xbrl.org/2003/instance" xmlns:xbrldi="http://xbrl.org/2006/xbrldi" xmlns:link="http://www.xbrl.org/2003/linkbase" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:iso4217="http://www.xbrl.org/2003/iso4217" xmlns:this="http://bsp.nbp.pl/BSP2_AR2_U/d-W020_SPORZ.xsd" xmlns:this1="http://bsp.nbp.pl/BSP2_AR2_U/p-BSP2_AR2_U.xsd" xmlns:this2="http://bsp.nbp.pl/BSP2_AR2_U/d-W030_RODZAJ.xsd" xmlns:this3="http://bsp.nbp.pl/BSP2_AR2_U/d-W040_OKRES.xsd" xmlns:this4="http://bsp.nbp.pl/BSP2_AR2_U/d-W050_NBP.xsd" xmlns:this5="http://bsp.nbp.pl/BSP2_AR2_U/d-W130_KRAJ.xsd" xmlns:this6="http://bsp.nbp.pl/BSP2_AR2_U/d-W140_POS_KRAJ.xsd" xmlns:this7="http://bsp.nbp.pl/BSP2_AR2_U/d-W160_TYP_TRAN.xsd" xmlns:this8="http://bsp.nbp.pl/BSP2_AR2_U/d-W170_STR_TRAN.xsd" xmlns:this9="http://bsp.nbp.pl/BSP2_AR2_U/d-W180_INICJOW.xsd" xmlns:this10="http://bsp.nbp.pl/BSP2_AR2_U/d-W190_ZDALNE.xsd" xmlns:this11="http://bsp.nbp.pl/BSP2_AR2_U/d-W200_SCHEMAT.xsd" xmlns:this12="http://bsp.nbp.pl/BSP2_AR2_U/d-W210_KARTY.xsd" xmlns:this13="http://bsp.nbp.pl/BSP2_AR2_U/d-W220_SCA.xsd" xmlns:this14="http://bsp.nbp.pl/BSP2_AR2_U/d-W250_CZY_OSZ.xsd" xmlns:this15="http://bsp.nbp.pl/BSP2_AR2_U/d-W320_ZKRES.xsd" xmlns:this16="http://bsp.nbp.pl/BSP2_AR2_U/d-W330_LICZ_WAR.xsd" xmlns:this17="http://bsp.nbp.pl/BSP2_AR2_U/d-W240_STR.xsd" xmlns:this18="http://bsp.nbp.pl/BSP2_AR2_U/d-W132_KRAJ.xsd" xmlns:this19="http://bsp.nbp.pl/BSP2_AR2_U/d-W280_MCC.xsd" xmlns:this20="http://bsp.nbp.pl/BSP2_AR2_U/d-W510_STR_TRAN2.xsd" xmlns:this21="http://bsp.nbp.pl/BSP2_AR2_U/d-W141_POS_KRAJ.xsd">
    <link:schemaRef xlink:type="simple" xlink:href="BSP2_AR2_UJK.xsd"/>
    <xbrli:context id="PayTel_fjk_20230930_ar2_1">
        <xbrli:entity>
            <xbrli:identifier scheme="https://sis2.nbp.pl/PayTel">60300</xbrli:identifier>
        </xbrli:entity>
        <xbrli:period>
            <xbrli:instant>{year + '-' + month + '-' + day}</xbrli:instant>
        </xbrli:period>
        <xbrli:scenario>
            <xbrldi:explicitMember dimension="this:W020_SPORZ">this:W020_KAR</xbrldi:explicitMember>
        </xbrli:scenario>
    </xbrli:context>
    <this1:MIMIE contextRef="PayTel_fjk_20230930_ar2_1">{values[0]}</this1:MIMIE>
    <this1:MNAZ contextRef="PayTel_fjk_20230930_ar2_1">{values[1]}</this1:MNAZ>
    <this1:MTEL contextRef="PayTel_fjk_20230930_ar2_1">{values[2]}</this1:MTEL>
    <this1:MEMAIL contextRef="PayTel_fjk_20230930_ar2_1">{values[3]}</this1:MEMAIL>
    <xbrli:context id="PayTel_fjk_20230930_ar2_2">
        <xbrli:entity>
            <xbrli:identifier scheme="https://sis2.nbp.pl/PayTel">60300</xbrli:identifier>
        </xbrli:entity>
        <xbrli:period>
            <xbrli:instant>2023-09-30</xbrli:instant>
        </xbrli:period>
        <xbrli:scenario>
            <xbrldi:explicitMember dimension="this:W020_SPORZ">this:W020_OSZ</xbrldi:explicitMember>
        </xbrli:scenario>
    </xbrli:context>
    <this1:MIMIE contextRef="PayTel_fjk_20230930_ar2_2">{values[0]}</this1:MIMIE>
    <this1:MNAZ contextRef="PayTel_fjk_20230930_ar2_2">{values[1]}</this1:MNAZ>
    <this1:MTEL contextRef="PayTel_fjk_20230930_ar2_2">{values[2]}</this1:MTEL>
    <this1:MEMAIL contextRef="PayTel_fjk_20230930_ar2_2">{values[3]}</this1:MEMAIL>
    <xbrli:unit id="unit1">
        <xbrli:measure>xbrli:pure</xbrli:measure>
	</xbrli:unit>
    """
    return code_ar2


def create_tabs(tab):
    path = 'Example\\'
    df = pd.read_excel(path + '2023_09_31_Q3___BSP_AR2_v.4.01_v2_no_PL_4arkusz_added_0.xlsx', sheet_name=tab[0], header=None, keep_default_na=False)

    codes = df.loc[30:, 0]
    countries = df.loc[27, 5:]

    additional_xml_code = ""
    number = 1
    year = '2023'
    month = '09'
    day = '30'

    for row, code in enumerate(codes):
        if code == '':
            continue
        else:
            print(code)
            if tab[0] == '5a.R.SF':
                countries = ['W0']

            for column, country in enumerate(countries):
                taxonomy = code.split('.')
                print(taxonomy, country)
# '4a.R.L_PLiW2', '4a.R.W_PLiW2', '5a.R.LF_PLiW2', '5a.R.WF_PLiW2'
                if tab[0] in ['4a.R.L_PLiW2', '4a.R.W_PLiW2', '5a.R.LF_PLiW2', '5a.R.WF_PLiW2']:
                    taxonomy[3] = country
                    value = df.iat[row + 30, column + 5]
                    if taxonomy[15] in ['M17', 'M19', 'M20']:
                        if value == '':
                            value = 0
                        unit = ['unit1', '2', format_decimal(value)]  # changed for PURE
                    else:
                        if value == '':
                            value = "0"
                        unit = ['unit1', '0', value]
                    xml = f"""
    <xbrli:context id="PayTel_fjk_{year + month + day}_{tab[1]}{number}">
        <xbrli:entity>
            <xbrli:identifier scheme="https://sis2.nbp.pl/PayTel">60300</xbrli:identifier>
        </xbrli:entity>
        <xbrli:period>
            <xbrli:instant>{year + '-' + month + '-' + day}</xbrli:instant>
        </xbrli:period>
        <xbrli:scenario>
            <xbrldi:explicitMember dimension="this2:W030_RODZAJ">this2:W030_{taxonomy[0]}</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="this3:W040_OKRES">this3:W040_{taxonomy[1]}</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="this4:W050_NBP">this4:W050_{taxonomy[2]}</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="this5:W130_KRAJ">this5:W130_{taxonomy[3]}</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="this6:W140_POS_KRAJ">this6:W140_{taxonomy[4]}</xbrldi:explicitMember>            
            <xbrldi:explicitMember dimension="this7:W160_TYP_TRAN">this7:W160_{taxonomy[5]}</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="this8:W170_STR_TRAN">this8:W170_{taxonomy[6]}</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="this9:W180_INICJOW">this9:W180_{taxonomy[7]}</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="this10:W190_ZDALNE">this10:W190_{taxonomy[8]}</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="this11:W200_SCHEMAT">this11:W200_{taxonomy[9]}</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="this12:W210_KARTY">this12:W210_{taxonomy[10]}</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="this13:W220_SCA">this13:W220_{taxonomy[11]}</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="this14:W250_CZY_OSZ">this14:W250_{taxonomy[12]}</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="this15:W320_ZKRES">this15:W320_{taxonomy[13]}</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="this16:W330_LICZ_WAR">this16:W330_{taxonomy[14]}</xbrldi:explicitMember>
        </xbrli:scenario>
    </xbrli:context>
    <this1:{taxonomy[15]} contextRef="PayTel_fjk_{year + month + day}_{tab[1]}{number}" unitRef="{unit[0]}" decimals="{unit[1]}">{unit[2]}</this1:{taxonomy[15]}>
                    """
# '5a.R.SF'
                elif tab[0] == '5a.R.SF':
                    value = df.iat[row + 30, 5]
                    if taxonomy[10] in ['M17', 'M19', 'M20']:
                        if value == '':
                            value = 0
                        unit = ['unit1', '2', format_decimal(value)]  # changed for PURE
                    else:
                        if value == '':
                            value = "0"
                        unit = ['unit1', '0', value]
                    xml = f"""
    <xbrli:context id="PayTel_fjk_{year + month + day}_{tab[1]}{number}">
        <xbrli:entity>
            <xbrli:identifier scheme="https://sis2.nbp.pl/PayTel">60300</xbrli:identifier>
        </xbrli:entity>
        <xbrli:period>
            <xbrli:instant>{year + '-' + month + '-' + day}</xbrli:instant>
        </xbrli:period>
        <xbrli:scenario>
            <xbrldi:explicitMember dimension="this2:W030_RODZAJ">this2:W030_{taxonomy[0]}</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="this3:W040_OKRES">this3:W040_{taxonomy[1]}</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="this4:W050_NBP">this4:W050_{taxonomy[2]}</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="this5:W130_KRAJ">this5:W130_W0</xbrldi:explicitMember>           
            <xbrldi:explicitMember dimension="this7:W160_TYP_TRAN">this7:W160_{taxonomy[4]}</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="this8:W170_STR_TRAN">this8:W170_{taxonomy[5]}</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="this17:W240_STR">this17:W240_{taxonomy[6]}</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="this14:W250_CZY_OSZ">this14:W250_{taxonomy[7]}</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="this15:W320_ZKRES">this15:W320_{taxonomy[8]}</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="this16:W330_LICZ_WAR">this16:W330_{taxonomy[9]}</xbrldi:explicitMember>
        </xbrli:scenario>
    </xbrli:context>
    <this1:{taxonomy[10]} contextRef="PayTel_fjk_{year + month + day}_{tab[1]}{number}" unitRef="{unit[0]}" decimals="{unit[1]}">{unit[2]}</this1:{taxonomy[10]}>

                    """

                elif tab[0] in ['6.ab.LiW']:
                    taxonomy[4] = country
                    value = df.iat[row + 30, column + 5]
                    if taxonomy[10] in ['M17', 'M19', 'M20']:
                        if value == '':
                            value = 0
                        unit = ['unit1', '2', format_decimal(value)]  # changed for PURE
                    else:
                        if value == '':
                            value = "0"
                        unit = ['unit1', '0', value]
                    xml = f"""
    <xbrli:context id="PayTel_fjk_{year + month + day}_{tab[1]}{number}">
        <xbrli:entity>
            <xbrli:identifier scheme="https://sis2.nbp.pl/PayTel">60300</xbrli:identifier>
        </xbrli:entity>
        <xbrli:period>
            <xbrli:instant>{year + '-' + month + '-' + day}</xbrli:instant>
        </xbrli:period>
        <xbrli:scenario>
            <xbrldi:explicitMember dimension="this2:W030_RODZAJ">this2:W030_{taxonomy[0]}</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="this3:W040_OKRES">this3:W040_{taxonomy[1]}</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="this4:W050_NBP">this4:W050_{taxonomy[2]}</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="this5:W130_KRAJ">this5:W130_{taxonomy[3]}</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="this6:W140_POS_KRAJ">this6:W140_{taxonomy[4]}</xbrldi:explicitMember>  
            <xbrldi:explicitMember dimension="this7:W160_TYP_TRAN">this7:W160_{taxonomy[5]}</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="this8:W170_STR_TRAN">this8:W170_{taxonomy[6]}</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="this9:W180_INICJOW">this9:W180_{taxonomy[7]}</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="this15:W320_ZKRES">this15:W320_{taxonomy[8]}</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="this16:W330_LICZ_WAR">this16:W330_{taxonomy[9]}</xbrldi:explicitMember>
        </xbrli:scenario>
    </xbrli:context>
    <this1:{taxonomy[10]} contextRef="PayTel_fjk_{year + month + day}_{tab[1]}{number}" unitRef="{unit[0]}" decimals="{unit[1]}">{unit[2]}</this1:{taxonomy[10]}>

                    """

                elif tab[0] in ['9.R.L.MCC', '9.R.W.MCC']:
                    taxonomy[3] = country
                    value = df.iat[row + 30, column + 5]
                    if value == '':
                        continue
                    else:
                        if taxonomy[10] in ['M17', 'M19', 'M20']:
                            unit = ['unit1', '2', format_decimal(value)]  # changed for PURE
                        else:
                            unit = ['unit1', '0', value]
                        if taxonomy[0] == "PMC":
                            if taxonomy[3] == 'D09':
                                xml = f"""
    <xbrli:context id="PayTel_fjk_{year + month + day}_{tab[1]}{number}">
        <xbrli:entity>
            <xbrli:identifier scheme="https://sis2.nbp.pl/PayTel">60300</xbrli:identifier>
        </xbrli:entity>
        <xbrli:period>
            <xbrli:instant>{year + '-' + month + '-' + day}</xbrli:instant>
        </xbrli:period>
        <xbrli:scenario>
            <xbrldi:explicitMember dimension="this2:W030_RODZAJ">this2:W030_{taxonomy[0]}</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="this3:W040_OKRES">this3:W040_{taxonomy[1]}</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="this4:W050_NBP">this4:W050_{taxonomy[2]}</xbrldi:explicitMember>
            <xbrldi:typedMember dimension="this18:W132_KRAJ"><this18:W132_KRAJREF>W130KRA0{taxonomy[3]}</this18:W132_KRAJREF></xbrldi:typedMember>
            <xbrldi:explicitMember dimension="this6:W140_POS_KRAJ">this6:W140_{taxonomy[4]}</xbrldi:explicitMember>  
            <xbrldi:explicitMember dimension="this10:W190_ZDALNE">this10:W190_{taxonomy[5]}</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="this19:W280_MCC">this19:W280_{taxonomy[6]}</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="this15:W320_ZKRES">this15:W320_{taxonomy[7]}</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="this16:W330_LICZ_WAR">this16:W330_{taxonomy[8]}</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="this20:W510_STR_TRAN2">this20:W510_{taxonomy[9]}</xbrldi:explicitMember>
        </xbrli:scenario>
    </xbrli:context>
    <this1:{taxonomy[10]} contextRef="PayTel_fjk_{year + month + day}_{tab[1]}{number}" unitRef="{unit[0]}" decimals="{unit[1]}">{unit[2]}</this1:{taxonomy[10]}>

                                """
                            else:
                                xml = f"""
    <xbrli:context id="PayTel_fjk_{year + month + day}_{tab[1]}{number}">
        <xbrli:entity>
            <xbrli:identifier scheme="https://sis2.nbp.pl/PayTel">60300</xbrli:identifier>
        </xbrli:entity>
        <xbrli:period>
            <xbrli:instant>{year + '-' + month + '-' + day}</xbrli:instant>
        </xbrli:period>
        <xbrli:scenario>
            <xbrldi:explicitMember dimension="this2:W030_RODZAJ">this2:W030_{taxonomy[0]}</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="this3:W040_OKRES">this3:W040_{taxonomy[1]}</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="this4:W050_NBP">this4:W050_{taxonomy[2]}</xbrldi:explicitMember>
            <xbrldi:typedMember dimension="this18:W132_KRAJ"><this18:W132_KRAJREF>W130KRA00{taxonomy[3]}</this18:W132_KRAJREF></xbrldi:typedMember>
            <xbrldi:explicitMember dimension="this6:W140_POS_KRAJ">this6:W140_{taxonomy[4]}</xbrldi:explicitMember>  
            <xbrldi:explicitMember dimension="this10:W190_ZDALNE">this10:W190_{taxonomy[5]}</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="this19:W280_MCC">this19:W280_{taxonomy[6]}</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="this15:W320_ZKRES">this15:W320_{taxonomy[7]}</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="this16:W330_LICZ_WAR">this16:W330_{taxonomy[8]}</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="this20:W510_STR_TRAN2">this20:W510_{taxonomy[9]}</xbrldi:explicitMember>
        </xbrli:scenario>
    </xbrli:context>
    <this1:{taxonomy[10]} contextRef="PayTel_fjk_{year + month + day}_{tab[1]}{number}" unitRef="{unit[0]}" decimals="{unit[1]}">{unit[2]}</this1:{taxonomy[10]}>

                                """
                        elif taxonomy[0] == "PCP":
                            if taxonomy[3] == 'D09':
                                xml = f"""
    <xbrli:context id="PayTel_fjk_{year + month + day}_{tab[1]}{number}">
        <xbrli:entity>
            <xbrli:identifier scheme="https://sis2.nbp.pl/PayTel">60300</xbrli:identifier>
        </xbrli:entity>
        <xbrli:period>
            <xbrli:instant>{year + '-' + month + '-' + day}</xbrli:instant>
        </xbrli:period>
        <xbrli:scenario>
            <xbrldi:explicitMember dimension="this2:W030_RODZAJ">this2:W030_{taxonomy[0]}</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="this3:W040_OKRES">this3:W040_{taxonomy[1]}</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="this4:W050_NBP">this4:W050_{taxonomy[2]}</xbrldi:explicitMember>
            <xbrldi:typedMember dimension="this18:W132_KRAJ"><this18:W132_KRAJREF>W130KRA0{taxonomy[3]}</this18:W132_KRAJREF></xbrldi:typedMember>
            <xbrldi:explicitMember dimension="this6:W140_POS_KRAJ">this6:W140_{taxonomy[4]}</xbrldi:explicitMember>         
            <xbrldi:explicitMember dimension="this7:W160_TYP_TRAN">this7:W160_{taxonomy[5]}</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="this8:W170_STR_TRAN">this8:W170_{taxonomy[6]}</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="this9:W180_INICJOW">this9:W180_{taxonomy[7]}</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="this10:W190_ZDALNE">this10:W190_{taxonomy[8]}</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="this11:W200_SCHEMAT">this11:W200_{taxonomy[9]}</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="this12:W210_KARTY">this12:W210_{taxonomy[10]}</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="this13:W220_SCA">this13:W220_{taxonomy[11]}</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="this14:W250_CZY_OSZ">this14:W250_{taxonomy[12]}</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="this15:W320_ZKRES">this15:W320_{taxonomy[13]}</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="this16:W330_LICZ_WAR">this16:W330_{taxonomy[14]}</xbrldi:explicitMember>
            
        </xbrli:scenario>
    </xbrli:context>
    <this1:{taxonomy[15]} contextRef="PayTel_fjk_{year + month + day}_{tab[1]}{number}" unitRef="{unit[0]}" decimals="{unit[1]}">{unit[2]}</this1:{taxonomy[15]}>

                                """
                            else:
                                xml = f"""
    <xbrli:context id="PayTel_fjk_{year + month + day}_{tab[1]}{number}">
        <xbrli:entity>
            <xbrli:identifier scheme="https://sis2.nbp.pl/PayTel">60300</xbrli:identifier>
        </xbrli:entity>
        <xbrli:period>
            <xbrli:instant>{year + '-' + month + '-' + day}</xbrli:instant>
        </xbrli:period>
        <xbrli:scenario>
            <xbrldi:explicitMember dimension="this2:W030_RODZAJ">this2:W030_{taxonomy[0]}</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="this3:W040_OKRES">this3:W040_{taxonomy[1]}</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="this4:W050_NBP">this4:W050_{taxonomy[2]}</xbrldi:explicitMember>
            <xbrldi:typedMember dimension="this18:W132_KRAJ"><this18:W132_KRAJREF>W130KRA00{taxonomy[3]}</this18:W132_KRAJREF></xbrldi:typedMember>
            <xbrldi:explicitMember dimension="this6:W140_POS_KRAJ">this6:W140_{taxonomy[4]}</xbrldi:explicitMember>         
            <xbrldi:explicitMember dimension="this7:W160_TYP_TRAN">this7:W160_{taxonomy[5]}</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="this8:W170_STR_TRAN">this8:W170_{taxonomy[6]}</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="this9:W180_INICJOW">this9:W180_{taxonomy[7]}</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="this10:W190_ZDALNE">this10:W190_{taxonomy[8]}</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="this11:W200_SCHEMAT">this11:W200_{taxonomy[9]}</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="this12:W210_KARTY">this12:W210_{taxonomy[10]}</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="this13:W220_SCA">this13:W220_{taxonomy[11]}</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="this14:W250_CZY_OSZ">this14:W250_{taxonomy[12]}</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="this15:W320_ZKRES">this15:W320_{taxonomy[13]}</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="this16:W330_LICZ_WAR">this16:W330_{taxonomy[14]}</xbrldi:explicitMember>
    
        </xbrli:scenario>
    </xbrli:context>
    <this1:{taxonomy[15]} contextRef="PayTel_fjk_{year + month + day}_{tab[1]}{number}" unitRef="{unit[0]}" decimals="{unit[1]}">{unit[2]}</this1:{taxonomy[15]}>

                                """

                additional_xml_code += xml
                number += 1
    return additional_xml_code


def add_geo(tab):
    countries = geo3_country
    tab_countries = geo3_country_loc

    path = 'Example\\'
    df = pd.read_excel(path + '2023_09_31_Q3___BSP_AR2_v.4.01_v2_no_PL_4arkusz_added_0.xlsx', sheet_name=tab, header=None, keep_default_na=False)

    codes = df.loc[30:, 0]

    additional_xml_code = ""
    number = 1

    year = '2023'
    month = '09'
    day = '30'

    for country_tab in tab_countries:
        for row, code in enumerate(codes):
            if code == '':
                continue
            else:
                print(code)
                for column, country in enumerate(countries):
                    taxonomy = code.split('.')
                    print(taxonomy, country)

                    value = df.iat[row + 30, column + 5]

                    if taxonomy[10] in ['M17', 'M19', 'M20']:
                        if value == 0:
                            value = "0.00"
                        unit = ['unit1', '2', value]  # changed for PURE
                    else:
                        unit = ['unit1', '0', value]

                    taxonomy[3] = country
                    taxonomy[4] = country_tab

                    xml = f"""
    <xbrli:context id="PayTel_fjk_{year + month + day}_{tab}_{country_tab}_{country}{number}">
        <xbrli:entity>
            <xbrli:identifier scheme="https://sis2.nbp.pl/PayTel">60300</xbrli:identifier>
        </xbrli:entity>
        <xbrli:period>
            <xbrli:instant>{year}-{month}-{day}</xbrli:instant>
        </xbrli:period>
        <xbrli:scenario>
            <xbrldi:explicitMember dimension="this2:W030_RODZAJ">this2:W030_{taxonomy[0]}</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="this3:W040_OKRES">this3:W040_{taxonomy[1]}</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="this4:W050_NBP">this4:W050_{taxonomy[2]}</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="this5:W130_KRAJ">this5:W130_{taxonomy[3]}</xbrldi:explicitMember>
            <xbrldi:typedMember dimension="this21:W141_POS_KRAJ"><this21:W141_POS_KRAJREF>W140POS00{taxonomy[4]}</this21:W141_POS_KRAJREF></xbrldi:typedMember>           
            <xbrldi:explicitMember dimension="this7:W160_TYP_TRAN">this7:W160_{taxonomy[5]}</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="this8:W170_STR_TRAN">this8:W170_{taxonomy[6]}</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="this9:W180_INICJOW">this9:W180_{taxonomy[7]}</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="this10:W190_ZDALNE">this10:W190_{taxonomy[8]}</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="this11:W200_SCHEMAT">this11:W200_{taxonomy[9]}</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="this12:W210_KARTY">this12:W210_{taxonomy[10]}</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="this13:W220_SCA">this13:W220_{taxonomy[11]}</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="this14:W250_CZY_OSZ">this14:W250_{taxonomy[12]}</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="this15:W320_ZKRES">this15:W320_{taxonomy[13]}</xbrldi:explicitMember>
            <xbrldi:explicitMember dimension="this16:W330_LICZ_WAR">this16:W330_{taxonomy[14]}</xbrldi:explicitMember>
        </xbrli:scenario>
    </xbrli:context>
    <this1:{taxonomy[15]} contextRef="PayTel_fjk_{year + month + day}_{tab}_{country_tab}_{country}{number}" unitRef="{unit[0]}" decimals="{unit[1]}">{unit[2]}</this1:{taxonomy[15]}>
    
                    """
                additional_xml_code += xml
                number += 1
    return additional_xml_code


if __name__ == '__main__':
    xml_code = ''
    xml_code += create_ar2(['Krzysztof', 'Kaniewski', '+48 506 297 621', 'krzysztof.kaniewski@paytel.pl'])

    EXCEL_READ_AR2 = [
        ['4a.R.L_PLiW2', '4a.R.L_PLiW2', '0'],
        ['4a.R.W_PLiW2', '4a.R.W_PLiW2', '1'],
        ['5a.R.LF_PLiW2', '5a.R.LF_PLiW2', '2'],
        ['5a.R.WF_PLiW2', '5a.R.WF_PLiW2', '3'],
        ['5a.R.SF', '5a.R.SF', '4'],
        ['6.ab.LiW', '6.ab.LiW', '5'],
        ['9.R.L.MCC', '9.R.L.MCC', '6'],
        ['9.R.W.MCC', '9.R.W.MCC', '7']
    ]
    for sheet in EXCEL_READ_AR2:
        xml_code += create_tabs(sheet)

    GEO3_TABS = [
        '4a.R.L_krajGEO3', '4a.R.W_krajGEO3', '5a.R.LF_krajGEO3', '5a.R.WF_krajGEO3'
    ]

    for sheet in GEO3_TABS:
        xml_code += add_geo(sheet)

    xml_code += '</xbrli:xbrl>'

    with open("PayTel_fjk_20230930_AR2.txt", 'w', encoding="utf-8") as file:
        file.write(xml_code)
