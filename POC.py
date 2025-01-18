import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation

#從 plotting 檢視表選取所有的資料
connection = sqlite3.connect("data/gapminder.db")
plotting_df = pd.read_sql("""SELECT * FROM plotting;""", con=connection)
connection.close()
#print(plotting_df.shape) 

# 透過 matplotlib 模組繪製動畫，先建立畫布跟軸物件
fig, ax = plt.subplots()
def update_plot(year_to_plot: int):
    ax.clear() #不保留前一圖表
    subset_df = plotting_df[plotting_df["dt_year"] == year_to_plot]
    #取y軸變數lex, x軸變數gdp_pcap, 顏色變數
    lex = subset_df["life_expectancy"].values
    gdp_pcap = subset_df["gdp_per_capita"].values
    cont = subset_df["continent"].values
    #print(subset_df["continent"].unique()) #['asia' 'europe' 'africa' 'americas']
    color_map = {
        "asia": "r",
        "africa": "g",
        "europe": "b",
        "americas": "c" #cyan
    }
    for xi, yi, ci in zip(gdp_pcap, lex, cont):
        ax.scatter(xi, yi, color=color_map[ci])
    ax.set_title(f"The world in {year_to_plot}")
    ax.set_xlabel("GDP Per Capita(in USD)")
    ax.set_ylabel("Life Expectancy")
    ax.set_ylim(20, 100) #界線設定20~100歲
    ax.set_xlim(0, 100000) #界線設定0~100000 USD per capita
# fig: 畫布物件。
# func: 更新軸物件的函數。
# frames: 要傳入 func 的數列。
# interval: 動畫間隔，以毫秒為單位。
# fps: 動畫每秒幀數
ani = animation.FuncAnimation(fig, func=update_plot, frames=range(2000, 2024), interval=10)
ani.save("animation.gif", fps=10)