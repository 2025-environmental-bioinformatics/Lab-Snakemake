import os
import pandas as pd
import numpy as np
import plotnine
import matplotlib.pyplot as plt

## read in the data

groundhog_data=pd.read_csv("../../data/groundhog-data.csv")

## create functions to parse data

def calculate_mean_groundhog(dataframe, shadow_column, shadow_condition, month_column):
    return np.mean(dataframe.loc[dataframe[shadow_column] == shadow_condition,month_column])
def calculate_sd_groundhog(dataframe, shadow_column, shadow_condition, month_column):
    return np.std(dataframe.loc[dataframe[shadow_column] == shadow_condition, month_column])

## calculate means and standard deviations for each shadow type

means=[]
stds=[]
months=[]
shadow=[]
for shadow_curr in ["Full","Partial","No"]:
    for month_curr in ["February","March"]:
        curr_mean=calculate_mean_groundhog(groundhog_data,"Punxsutawney Phil",
                                           shadow_curr+" Shadow",month_curr+" Average Temperature")
        curr_std=calculate_sd_groundhog(groundhog_data,"Punxsutawney Phil",
                                        shadow_curr+" Shadow",month_curr+" Average Temperature")
        means.append(curr_mean)
        stds.append(curr_std)
        months.append(month_curr)
        shadow.append(shadow_curr)
        

## calculate the change between February and March temperatures

Full_Shadow=groundhog_data.loc[groundhog_data["Punxsutawney Phil"] == "Full Shadow"]
Partial_Shadow=groundhog_data.loc[groundhog_data["Punxsutawney Phil"] == "Partial Shadow"]
No_Shadow=groundhog_data.loc[groundhog_data["Punxsutawney Phil"] == "No Shadow"]

Difference_Partial_Shadow=Partial_Shadow["March Average Temperature"]-Partial_Shadow["February Average Temperature"]
Difference_Full_Shadow=Full_Shadow["March Average Temperature"]-Full_Shadow["February Average Temperature"]
Difference_No_Shadow=No_Shadow["March Average Temperature"]-No_Shadow["February Average Temperature"]

## DO NOT READ THIS CODE - SAVE & PLOT RESULTS ##

shadow_predictions=pd.DataFrame({"Shadow":shadow,
                                 "Month":months,
                                 "Mean":means,
                                 "StDev":stds})

def get_shadow_predict(prediction,month,mean_or_std):
    return float(shadow_predictions.loc[(shadow_predictions.Month==month)&(shadow_predictions.Shadow==prediction),mean_or_std])
print("")
print("################OUTPUT SUMMARY#################")
print("")
print("When the Groundhog saw its shadow, mean air temperatures were\n",
      get_shadow_predict(prediction="Full",month="February",mean_or_std="Mean"),
      "+/-",get_shadow_predict(prediction="Full",month="February",mean_or_std="StDev"),
      "in February and\n",get_shadow_predict(prediction="Full",month="March",mean_or_std="Mean"),"+/-",
      get_shadow_predict(prediction="Full",month="March",mean_or_std="StDev"),"in March.")
print("")
print("When the Groundhog did not see its shadow, mean air temperatures were\n",
      get_shadow_predict(prediction="No",month="February",mean_or_std="Mean"),
      "+/-",get_shadow_predict(prediction="No",month="February",mean_or_std="StDev"),
      "in February and\n",get_shadow_predict(prediction="No",month="March",mean_or_std="Mean"),
      "+/-",get_shadow_predict(prediction="No",month="March",mean_or_std="StDev"),"in March.")
print("")
print("###############################################")
print("")

if not os.path.exists("../results"):
    os.mkdir("../results")

## sees shadow = predict 6 more weeks of winter

barplot_df=shadow_predictions
barplot_df["UpperError"] = [curr+stdev for curr,stdev in zip(barplot_df.Mean,barplot_df.StDev)]
barplot_df["LowerError"] = [curr-stdev for curr,stdev in zip(barplot_df.Mean,barplot_df.StDev)]

barplot_df_cat = pd.Categorical(barplot_df['Shadow'], categories=["No","Partial","Full"])
barplot_df = barplot_df.assign(ShadowCat = barplot_df_cat)

shadow_plot = (plotnine.ggplot(barplot_df) + 
     plotnine.geom_bar(plotnine.aes(x="ShadowCat",y="Mean",fill="Month"),stat="identity",position="dodge")+
     plotnine.geom_errorbar(plotnine.aes(x="ShadowCat",ymin="LowerError",ymax="UpperError",
                                         group="Month"),stat="identity",
                            position=plotnine.position_dodge(width=0.9))+
     plotnine.theme_bw(base_size=12) + plotnine.xlab("Shadow seen") + 
     plotnine.scale_fill_manual(name="Month",values=["orange","purple"]) +
     plotnine.ylab("Mean air temperature") + plotnine.ggtitle("When the groundhog sees his shadow\nis it 6 more weeks of winter?"))

plotnine.ggsave(shadow_plot,filename="../results/shadow_results.png")

plt.boxplot(labels = ["No","Partial","Full"],#["Full"]*len(Difference_Full_Shadow), 
            x = [[curr for curr in Difference_No_Shadow if curr==curr],
                 [curr for curr in Difference_Partial_Shadow if curr==curr],
                 [curr for curr in Difference_Full_Shadow if curr==curr]],positions=range(3))

plt.scatter(x = ["No"]*len(Difference_No_Shadow), y = Difference_No_Shadow)
plt.scatter(x = "Partial", y = Difference_Partial_Shadow,)
plt.scatter(x = ["Full"]*len(Difference_Full_Shadow), y = Difference_Full_Shadow)
plt.xlabel('Shadow level')
plt.ylabel('Difference between March\nand February temperatures')
plt.savefig('../results/shadow_boxplots.png')
plt.show()
