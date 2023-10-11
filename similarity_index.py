import numpy as np

def similarity_index(Combined_cleaned,Package_info_ST,Package_info_NXP,Renesas_combined_cores,competitor_part_number,Core_comparison,a=2,b=2,c=2,d=1,e=1,f=1):
    competitor_freq =list(Combined_cleaned[Combined_cleaned["Part Number"] == competitor_part_number]["Frequency Scaled"])[0]
    competitor_RAM =list(Combined_cleaned[Combined_cleaned["Part Number"] == competitor_part_number]["RAM Size (kB)"])[0]
    competitor_Flash =list(Combined_cleaned[Combined_cleaned["Part Number"] == competitor_part_number]["Flash Size (kB) (Prog)"])[0]
    competitor_lead =list(Combined_cleaned[Combined_cleaned["Part Number"] == competitor_part_number]["Lead Count (#)"])[0]
    competitor_core =list(Combined_cleaned[Combined_cleaned["Part Number"] == competitor_part_number]["Core"])[0]

    oui= ["Frequency_similarity_index","RAM_similarity_index","Flash_similarity_index","Lead_count_similarity_index","Pkg_similarity_index","Core_similarity_index"]
     
    
    Renesas_combined_cores.loc[:,"Frequency_similarity_index"] =  Renesas_combined_cores.loc[:,"Frequency Scaled"].apply(lambda x: ((np.min([x,competitor_freq]))/(np.max([x,competitor_freq]))))
    Renesas_combined_cores.loc[:,"RAM_similarity_index"] =  Renesas_combined_cores.loc[:,"RAM Size (kB)"].apply(lambda x: ((np.min([x,competitor_RAM]))/(np.max([x,competitor_RAM]))) )
    Renesas_combined_cores.loc[:,"Flash_similarity_index"] =  Renesas_combined_cores.loc[:,"Flash Size (kB) (Prog)"].apply(lambda x: ((np.min([x,competitor_Flash]))/(np.max([x,competitor_Flash]))) )
    Renesas_combined_cores.loc[:,"Lead_count_similarity_index"] =  Renesas_combined_cores.loc[:,"Lead Count (#)"].apply(lambda x: ((np.min([x,competitor_lead]))/(np.max([x,competitor_lead]))) )
    Renesas_combined_cores.loc[:,"Core_similarity_index"] = Renesas_combined_cores.loc[:,"Core"].apply(lambda x:int(Core_comparison.loc[x][competitor_core]))
    
    pkg_names = Combined_cleaned[Combined_cleaned["Part Number"] == competitor_part_number]["Pkg. Type"].unique()
    company_name = Combined_cleaned[Combined_cleaned["Part Number"] == competitor_part_number]["Company"].tolist()[0]
    package_info_index = Package_info_ST.index.values.tolist()
    workable_package = []
    

    if ~Combined_cleaned[Combined_cleaned["Part Number"] == competitor_part_number]["Pkg. Type"].any():
        Renesas_combined_cores.loc[:,"Pkg_similarity_index"] = 0
        
    elif company_name == "STM":
        for j in package_info_index:
            for i in pkg_names:
                if int(Package_info_ST.loc[[j]][i]) == 1:
                    workable_package.append(j)
    
    else:
        for j in package_info_index:
            for i in pkg_names:
                if int(Package_info_NXP.loc[[j]][i]) == 1:
                    workable_package.append(j)        
    
    for i in Renesas_combined_cores.index: 
        if Renesas_combined_cores.loc[i,"Pkg. Type"] in workable_package:
            Renesas_combined_cores.loc[i,"Pkg_similarity_index"] = 1
        else:
            Renesas_combined_cores.loc[i,"Pkg_similarity_index"] = 0
    
    
    Renesas_combined_cores.loc[: , oui] = Renesas_combined_cores[oui].fillna(0)
    for i in Renesas_combined_cores.index:
        columns = list(Renesas_combined_cores.loc[i,oui])
        Renesas_combined_cores.loc[i,"Similarity_Index"] = np.average(columns,weights= [a,b,c,d,e,f])
    
    return Renesas_combined_cores.sort_values(by = "Similarity_Index",ascending=False)
