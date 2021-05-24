from sdg.open_sdg import open_sdg_build
import pandas as pd
import http

tier_spreadsheet_url = 'https://unstats.un.org/sdgs/files/Tier%20Classification%20of%20SDG%20Indicators_28%20Dec%202020_web.xlsx'

while True:
    try:
        tier_df = pd.read_excel(tier_spreadsheet_url, "Updated Tier classification", usecols=[2,6], names=['indicator', 'tier'], header=1).dropna(axis=0, subset=["indicator"])
        tier_df=tier_df[tier_df["indicator"]!="\n"]
        for i in tier_df.index:
            indicator_code=tier_df.loc[i, "indicator"]
            tier_df.loc[i, "indicator"]=indicator_code.split(" ")[0]
        tier_df = tier_df.set_index(['indicator'])
        break
    except http.client.RemoteDisconnected as e:
        continue
        


archive_types = {
    "deleted": "This indicator was deleted following <a href='https://sdgdata.gov.uk/updates/2021/02/17/2020-indicator-changes.html'>indicator changes</a> from the United Nations 2020 Comprehensive Review.",
    "replaced": "This indicator was replaced following <a href='https://sdgdata.gov.uk/updates/2021/02/17/2020-indicator-changes.html'>indicator changes</a> from the United Nations 2020 Comprehensive Review.",
    "revised": "This indicator was revised following <a href='https://sdgdata.gov.uk/updates/2021/02/17/2020-indicator-changes.html'>indicator changes</a> from the United Nations 2020 Comprehensive Review."
}

change_types = {
    "revised": "This indicator was revised following <a href='https://sdgdata.gov.uk/updates/2021/02/17/2020-indicator-changes.html'>indicator changes</a> from the United Nations 2020 Comprehensive Review. The indicator from before these revisions has been <a href='https://sdgdata.gov.uk/archived-indicators'>archived</a>.",
    "replaced": "This indicator was added following <a href='https://sdgdata.gov.uk/updates/2021/02/17/2020-indicator-changes.html'>indicator changes</a> from the United Nations 2020 Comprehensive Review. The indicator it replaced has been <a href='https://sdgdata.gov.uk/archived-indicators'>archived</a>.",
    "moved": "This indicator was moved following <a href='https://sdgdata.gov.uk/updates/2021/02/17/2020-indicator-changes.html'>indicator changes</a> from the United Nations 2020 Comprehensive Review. The indicator it replaced has been <a href='https://sdgdata.gov.uk/archived-indicators'>archived</a>."
}

archived_indicators=pd.read_csv('archived_indicators.csv')
changed_indicators=pd.read_csv('changed_indicators.csv')

def my_indicator_id_alteration(indicator_id, context):
    if indicator_id is not None and context['meta'] is not None:
        if "archived" in indicator_id:
             indicator_id="archived_indicator_"+context['meta']['indicator_number'].replace(".","-")
    return indicator_id




        
  
open_sdg_build(config='config_data.yml', alter_indicator_id=my_indicator_id_alteration)

