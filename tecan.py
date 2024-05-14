
import pandas as pd
import math

class tecan:
    """
    Class to handle Tecan Spark Files. 
    Attribues are file name, plate data frame and settings_indexes. These are the indexes (or rows)
    in column 1 where the cell lists the absorbance wavelength as a string in the fromat abs_read,
    e.g. '260_read'
    """
    file_type = 'xlsx' 
    
    def __init__(self, name: str):
        """
        Initializes attributes of tecan instance Takes in the name of the Tecan Spark xlsx file 
        """
        self.name = name 
        self.plate = pd.read_excel(self.name, usecols = 'A, B, C, D, E', header=None)
        self.settings_indexes = self.plate[self.plate[1].str.contains('_read', na=False)].index.tolist()
        
    def read_tecan_params(self) -> pd.DataFrame:
        """
        Subsets the plate attribute dataframe
        Returns a tecan parameters dataframe 
        """
        df = self.plate.iloc[0:14, [0, 4]]
        df = df.dropna(how='all')
        df = df.rename(columns={0:'settings', 4:'values'})
        df.loc[0, 'values'] = df.loc[0, 'settings'].split(':')[1]
        df.loc[0, 'settings'] = df.loc[0, 'settings'].split(':')[0]
        
        return df
        
    def read_wl_settings(self) -> pd.DataFrame:
        """
        Subsets the plate attribute dataframe
        Returns a data frame of the settings used for each wavelengh 
        """
        df = pd.DataFrame()
        
        for i in self.settings_indexes:
            df_settings = self.plate.iloc[i-1:i+8, [0,1,4]]
            df_settings[1] = df_settings[1].fillna(df_settings[4])
            df_settings = df_settings[[0, 1]]
            df_settings = df_settings.dropna(how = 'all')
            df_settings['wavelength'] = self.plate.loc[i, 1].split('_')[0]
            df_settings = df_settings.rename(columns={0:'settings', 1:'value'})
            df = pd.concat([df, df_settings], ignore_index=True)

        return df
    
        
class  wl_data(tecan):
    """
    Child class of tecan class
    """
    def __init__(self, name):
        """
        Inherrits attribues and methods from tecan class
        """
        tecan.__init__(self, name) 
    
    def data(self) -> pd.DataFrame:
        """
        Grabs the absorbance data from the plate attribute 
        using the settings_indexes attribute to find data for each wavelength 
        Returns a data frame with Well Positions and Absorbances, e.g.
        
        Well Positions    260_read    320_read
               A1           0.1119     0.0459
               B1           0.1282     0.0459
               C1           0.124      0.0454
               D1           0.1306     0.0457
               E1           0.1253     0.0456
        """
        
        indexes = self.settings_indexes
        plate = self.plate
        df = pd.DataFrame(columns=['Well Positions'])
        #set_trace()
        for i in indexes:
    
            wl = plate.iloc[i, 1]
            data2 = plate.iloc[i+10:i+106, [0,1]].reset_index(drop=True)
            data2 = data2.rename(columns={0:'Well Positions', 1:wl})
            df = df.merge(data2, on='Well Positions', how='outer')
            
        return df
