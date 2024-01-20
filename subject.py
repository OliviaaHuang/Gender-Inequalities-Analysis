# Step 1 Import libraries
import pandas as pd
import os
from pyecharts.charts import Bar
from pyecharts import options as opts
from pyecharts.charts import Bar3D

# Step 2 Import dataset
def get_data():
    df = pd.read_csv(config['data'], header=13, dtype=str)
    df['Academic Year'] = df['Academic Year'].apply(lambda x: x[:4])
    return df

# Step 3 Data visualization
def set_bar3d(x_data, data, year):
    y_data = ['male', 'female']
    bar = Bar3D(init_opts=opts.InitOpts(
        width='1500px', height='1000px', page_title='探究%s年男女生喜欢课程' % year)
    )
    bar.add(
        series_name="",
        data=[[d[0], d[1], d[2]] for d in data],
        xaxis3d_opts=opts.Axis3DOpts(
            data=x_data, type_="category",
            name='subject', is_show=True,
            axislabel_opts=opts.LabelOpts(rotate=30, interval=0)),
        yaxis3d_opts=opts.Axis3DOpts(data=y_data, type_="category", name='sex'),
        zaxis3d_opts=opts.Axis3DOpts(type_="value", name='人数'),
    )
    bar.set_global_opts(
        visualmap_opts=opts.VisualMapOpts(
            max_=70000,
            range_color=
            ["#313695",
             "#4575b4",
             "#74add1",
             "#abd9e9",
             "#e0f3f8",
             "#ffffbf",
             "#fee090",
             "#fdae61",
             "#f46d43",
             "#d73027",
             "#a50026", ]
        ),
        title_opts=opts.TitleOpts(title="探究男生女生喜欢课程的人数")
    )
    bar.render('%s年男女喜欢课程人数.html' % year)


def set_bar_chart(subjects, male, female, year):
    title = "Gender data by subject in %s" % year
    c = (
        Bar(init_opts=opts.InitOpts(
            width="1500px", height="800px", page_title=title)
        )
        .add_xaxis(subjects)
        .add_yaxis('male', male)
        .add_yaxis("female", female)
        .reversal_axis()
        .set_series_opts(label_opts=opts.LabelOpts(position="right"))
        .set_global_opts(title_opts=opts.TitleOpts(title=title))
    )
    c.render('%s.html' % title)
    return c


def main():
    df = get_data()
    subjects = list(set(df['CAH level 1'].to_list()))
    for year in range(2019, 2023):
        _df = df[df['Academic Year'] == str(year)]
        male = list()
        female = list()
        for index, value in enumerate(subjects):
            number = _df[(_df['CAH level 1'] == value) & (_df['Sex'] == 'Male')]['Number'].values
            if number.size:
                number = number[0]
                male.append(int(number))
            number = _df[(_df['CAH level 1'] == value) & (_df['Sex'] == 'Female')]['Number'].values
            if number.size:
                number = number[0]
                female.append(int(number))
        # set_bar3d(subjects, result, year)
        set_bar_chart(subjects, male, female, year)
script_directory = os.path.dirname(os.path.abspath(__file__))

config = {
    'data': os.path.join(script_directory, 'gender.csv')
}

if __name__ == '__main__':
    main()
