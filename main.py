
import pandas as pd
import requests
import json
import pyecharts
import os
from pyecharts.charts import Line
from collections import defaultdict
from pyecharts.commons.utils import JsCode
from pyecharts.globals import ChartType
from pyecharts.charts import Map3D
from pyecharts import options as opts



def get_lang_latitude():
    df = pd.read_csv(config['location'])
    result = {}
    for index in range(df.shape[0]):
        result[df.loc[index, 'en']] = [df.loc[index, '经度'], df.loc[index, '维度'], 0]
    return result


def get_year_data():

    df = pd.read_csv(config['student_src'], header=13, dtype=str)
    df['Academic Year'] = df['Academic Year'].apply(lambda x: x[:4])
    result = defaultdict(list)
    for index in range(df.shape[0]):
        result[df.loc[index, 'Country of study']].append({
            df.loc[index, 'Academic Year']: df.loc[index, 'Number']
        })
    return result


def set_map(data, year):
    map2 = Map3D(init_opts=opts.InitOpts(
        width='1500px', height='1000px', page_title="%s source of student" % year))
    map2.add_schema(
        maptype='world',
        itemstyle_opts=opts.ItemStyleOpts(
            color="rgb(5,101,123)",
            opacity=1,
            border_width=0.8,
            border_color="rgb(62,215,213)",
        ),
        map3d_label=opts.Map3DLabelOpts(
            is_show=False,
            formatter=JsCode(
                "function(data){return data.name + " " + data.value[2];}"),
        ),
        emphasis_label_opts=opts.LabelOpts(
            is_show=False,
            color="#fff",
            font_size=10,
            background_color="rgba(0,23,11,0)",
        ),
        light_opts=opts.Map3DLightOpts(
            main_color="#fff",
            main_intensity=1.2,
            main_shadow_quality="high",
            is_main_shadow=False,
            main_beta=10,
            ambient_intensity=0.3,
        ),
    ).add(
        series_name="source of student",
        data_pair=data,
        type_=ChartType.BAR3D,
        bar_size=1,
        shading="lambert",
        label_opts=opts.LabelOpts(
            is_show=False,
            formatter=JsCode(
                "function(data){return data.name + ' ' + data.value[2];}"),
        ),
    ).set_global_opts(title_opts=opts.TitleOpts(title="%s source of student" % year))
    return map2


def get_lat_lang_via_year(year, data):
    """
    :param year: 2014
    :param data: [{'2014': 10}, {'2014': 10}]
    :return:
    """
    for kv in data:
        if str(year) in kv:
            return kv[year]
    return 0


def get_country_location(country, areas):
    """生源地区中含有Hong Kong (xxx)这样的数据
    """
    location = areas.get(country, None)
    if location is not None:
        return location
    for key in areas:
        if country.startswith(key):
            return areas[key]
    return None


def get_number_with_year(year, data):
    for kv in data:
        num = kv.get(str(year), 0)
        if num:
            return num
    return 0


def main():
    year_data = get_year_data()
    areas = get_lang_latitude()

    line = Line(init_opts=opts.InitOpts(
        width='1500px', height='1000px', page_title="Enrollment change"))
    line.set_global_opts(
        title_opts=opts.TitleOpts(title="the change of student"),
        xaxis_opts=opts.AxisOpts(type_="category", name="year"),
        yaxis_opts=opts.AxisOpts(type_="value", name="the number of student"),
    )

    for country in year_data:
        data = []
        for year in range(2014, 2022):
            number = int(get_number_with_year(year, year_data[country]))
            data.append({"year": str(year), "value": number})

        line.add_xaxis([x["year"] for x in data])
        line.add_yaxis(country, [opts.LineItem(name=x["year"], value=x["value"]) for x in data], label_opts=opts.LabelOpts(is_show=False))

    line.render("Line chart of changes in enrollment by country.html")

    for year in range(2014, 2022):
        data = list()
        for country in year_data:
            # {'China': [{'2014': 3}]}
            location = get_country_location(country, areas)
            if location is not None:
                location[-1] = int(get_number_with_year(year, year_data[country]))
                data.append((country, location))
            else:
                print('%s无对应坐标' % country)
        _map = set_map(data, year)
        _map.render('International enrollment in %s.html' % year)

script_directory = os.path.dirname(os.path.abspath(__file__))


config = {
    'location': os.path.join(script_directory, 'Latitude and longitude.csv'),
    'student_src': os.path.join(script_directory, 'students’ place of origin.csv')
}


if __name__ == '__main__':
    main()