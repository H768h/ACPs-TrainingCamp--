"""
1960-2019年全球各国GDP的变化柱状图开发
"""

from pyecharts.charts import Bar, Timeline
from pyecharts.options import *
from pyecharts.globals import ThemeType

# 文件处理
f = open("D:/python_study/1960-2019全球GDP数据.csv", "r", encoding="GB2312")
data_lines = f.readlines()
f.close()

# 将数据转化为{年份：[[国家，gdp], [], ...], 年份:[[国家， gdp], [], ...], ...}形式的字典
# 删除第一条数据
del data_lines[0]
# 将数据转化为字典
data_dict = {}
for line in data_lines:
    year = int(line.split(",")[0])          # 年份
    country = line.split(",")[1]            # 国家
    gdp = float(line.split(",")[2])         # gdp数据
    # 判断字典中有没有存在的year并做出相应的代码执行
    try:
        data_dict[year].append([country, gdp])
    except KeyError:
        data_dict[year] = []
        data_dict[year].append([country, gdp])

# 对字典年份进行排序（原因是字典无序）
sorted_year_list = sorted(data_dict.keys())

# 构建时间线柱状图并设置主题
timeline = Timeline({"theme": ThemeType.LIGHT})
for year in sorted_year_list:
    data_dict[year].sort(key=lambda element: element[1], reverse=True)

    # 取出本年份前8名的国家
    year_data = data_dict[year][:8]
    x_data = []
    y_data = []
    for country_gdp in year_data:
        x_data.append(country_gdp[0])            # X轴添加国家
        y_data.append(country_gdp[1]/100000000)         # Y轴添加gdp数据

    # 构建柱状图的对象
    bar = Bar()
    x_data.reverse()         # 数据反转
    bar.add_xaxis(x_data)
    bar.add_yaxis("GDP(亿)", y_data[::-1], label_opts=LabelOpts(position="right"))
    bar.reversal_axis()

    # 设置每一年的图标的标题
    bar.set_global_opts(
        title_opts=TitleOpts(title=f"{year}年全球前八GDP数据")
    )
    timeline.add(bar, str(year))

# 设置时间线的自动播放
timeline.add_schema(
    play_interval=1000,
    is_timeline_show=True,
    is_loop_play=False,
    is_auto_play=True
)

# 绘图
timeline.render("1960-2019年全球GDP前八国家.html")