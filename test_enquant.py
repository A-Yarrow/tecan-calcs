# from Absorbance_Quant_ENC_Data import make_data_table
# from Absorbance_Quant_ENC_Data import adder
import pytest
import Absorbance_Quant_ENC_Data as aqe
#import pytest
import pandas as pd


def test_calculate_enrichment_quant():
    assert aqe.calculate_enrichment_quant(abs1 = 0.1119, abs2 = 0.0459, volume=50.0) == 2.90

    #import pdb; pdb.set_trace()
    
#Practice functions    

#@pytest.fixture()
#def setup():
#    return pd.DataFrame({"a": [1,2,3]})

#def test_adder_basic(setup):
#    import pdb; pdb.set_trace()
#    my_value = setup.iloc[0,0]
#    assert adder(1, 0)  ==  my_value

#my_inputs = [1,2,3,4,5]

#@pytest.mark.parametrize("inx_number", my_inputs)
#def test_adder_param(inx_number):
#    assert adder(1, inx_number)  ==  inx_number + 1

#    expected = 6
#    assert adder(1, 5)  ==  expected
#def test_expect_error():
#    with pytest.raises(TypeError):
#        adder(5,  "5")

