import pandas as pd
import math
import argparse
from datetime import datetime
from tecan import wl_data

def calculate_enrichment_quant(abs1: float, abs2: float, volume: float = 50.0) -> float:
    """
    Reads in abs1 and abs2 (baseline wavelength) and Returns concentration as a float
    """

    concentration = ((abs1 - abs2) * math.pi * 4.69 ** 2 / (0.008 * volume)) - 8.5
    concentration = round(concentration, 2)
    return concentration


def make_enr_quant_table(data: pd.DataFrame, w1: str, w2: str,
                         volume: float = 50.0) -> pd.DataFrame:
    """
    Reads in Tecan absorbance pandas dataframe from the data method of the wl_data class
    e.g.
    file = wl_data(name='LUNAR2_ENQ_v1_0_0_20220914_114347.xlsx')
    data = file.data() expecting
    dataframe format:

    Well Positions    260_read    320_read
          A1           0.1119      0.0459
          B1           0.1282      0.0459
          C1           0.124       0.0454
          D1           0.1306      0.0457
          E1           0.1253      0.0456
          ...          ...         ...
          D12          0.1042      0.0464
          E12          0.1035      0.0467
          F12          0.1045      0.0468
          G12          0.2359      0.1694
          H12          0.1094      0.0464


    Calls calculate_enrichment_quantto calculate enrichment concentrations.
    w2 is the background wavelength. w2 is subtracted from w1.
    Returns an Absorbance Quant ENC data table with Enrichment Quant calculations.
    """

    df = data.copy()
    df.index += 1
    df['Volume'] = volume
    df['Concentration (ng/uL)'] = df.apply(lambda row: calculate_enrichment_quant(row[w1], row[w2], row['Volume']),
                                           axis=1)
    df['Total DNA (ng)'] = df['Volume'] * df['Concentration (ng/uL)']

    # USER ENTERED COLUMNS
    df['Pool For AutoPooling'] = ''
    df['Sample ID'] = ''

    return df

def write_out_quants(df)->str:
    """
    Writes out a file containing EN Quants
    and returns name of output file
    """
    now = datetime.now()
    now_string = now.strftime("%d%m%Y")
    file_out = 'enr_quant_out'+'_'+ now_string + '.tsv'
    df.to_csv(file_out, sep='\t')
    return file_out

def parse_arguments():

    parser = argparse.ArgumentParser()
    parser.add_argument("-w1", "--wavelength1", default="A260_read", help="Wavelength_read to measure, e.g. A260_read")
    parser.add_argument("-w2", "--wavelength2", default="A320_read", help="Wavelength_read to subtract, e.g. A320_read")
    parser.add_argument("-f", "--excel_file", help='name of xlsx file' )

    args = parser.parse_args()
    return args

def main():

    args = parse_arguments()
    w1 = args.wavelength1
    w2 = args.wavelength2

    excel_file = args.excel_file

    file = wl_data(name=excel_file)
    data = file.data()
    table = make_enr_quant_table(data, w1=w1, w2=w2)
    file_out = write_out_quants(table)
    print('Quant table written out to file %s'%(file_out))

if __name__=="__main__":
    main()
    
