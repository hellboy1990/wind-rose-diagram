#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from pyecharts.globals import CurrentConfig
from pyecharts import options as opts
from pyecharts.charts import Radar
import pandas as pd
import operator
import numpy as np
import json
CurrentConfig.ONLINE_HOST = 'D:\\01Installation Package\\pyecharts-assets-master\\assets\\'


def count_seasons(labs, oris):  # 统计不同季节的风频
    # labs_index = labs.index.to_list()
    # print(labs_index)
    springms, summerms, autumnms, winterms = [3, 4, 5], [6, 7, 8], [9, 10, 11], [12, 1, 2]
    springs, summers, autumns, winters = labs[springms], labs[summerms], labs[autumnms], labs[winterms]
    # print(summers)
    seasons4 = [[] for n in range(5)]
    for i in range(len(oris)):
        # print(i)
        seasons4[0].append(sum(list(springs.iloc[i])))  # 取第i行数据，转为列表，求和
        # print(list(springs.iloc[i]))
        seasons4[1].append(sum(list(summers.iloc[i])))  # 取第i行数据，转为列表，求和
        seasons4[2].append(sum(list(autumns.iloc[i])))  # 取第i行数据，转为列表，求和
        seasons4[3].append(sum(list(winters.iloc[i])))  # 取第i行数据，转为列表，求和
        seasons4[4].append(sum(list(labs.iloc[i])))  # 取第i行数据，转为列表，求和(逐年)
    # 四季单独统计
    season1 = pd.DataFrame(seasons4[0])
    season2 = pd.DataFrame(seasons4[1])
    season3 = pd.DataFrame(seasons4[2])
    season4 = pd.DataFrame(seasons4[3])
    season1_4 = pd.DataFrame(seasons4[4])
    season1.index, season2.index, season3.index, season4.index, season1_4.index = oris, oris, oris, oris, oris  # 索引
    # season1.index = labs_index  # 设置行索引
    # print(season1)
    # # 四季并列统计
    # df_seasons4 = pd.DataFrame(seasons4).T
    # df_seasons4.columns = ['spring', 'summer', 'autumn', 'winter']
    # df_seasons4.index = labs_index
    # print(df_seasons4)
    return season1, season2, season3, season4, season1_4


def draw_radar(season_x, season_name, filechart, seasonareacolor, seasonlinecolor):
    # 建立schema的json文件  season_x.columns = [season_name]
    season_index = season_x.index.to_list()
    # print(season_index)
    # n_max, n_min = max(season_x), min(season_x)
    n_max = max(enumerate(season_x[0]), key=operator.itemgetter(1))[1]
    n_min = min(enumerate(season_x[0]), key=operator.itemgetter(1))[1]
    # 用于获取对象的哪些维的数据
    # print(n_max, n_min)
    df_season = pd.DataFrame({'name': season_index})
    df_season['max'], df_season['min'] = n_max, n_min
    # season_js = df_season.to_json(orient='records')
    # print(season_js)
    # 设置16方位, 逆时针排序
    season_js = [
        {"name": "N", "max": n_max, "min": n_min},
        {"name": "NNW", "max": n_max, "min": n_min},
        {"name": "NW", "max": n_max, "min": n_min},
        {"name": "WNW", "max": n_max, "min": n_min},
        {"name": "W", "max": n_max, "min": n_min},
        {"name": "WSW", "max": n_max, "min": n_min},
        {"name": "SW", "max": n_max, "min": n_min},
        {"name": "SSW", "max": n_max, "min": n_min},
        {"name": "S", "max": n_max, "min": n_min},
        {"name": "SSE", "max": n_max, "min": n_min},
        {"name": "SE", "max": n_max, "min": n_min},
        {"name": "ESE", "max": n_max, "min": n_min},
        {"name": "E", "max": n_max, "min": n_min},
        {"name": "ENE", "max": n_max, "min": n_min},
        {"name": "NE", "max": n_max, "min": n_min},
        {"name": "NNE", "max": n_max, "min": n_min},
    ]
    # 设置数据
    fengsus = season_x[0].to_list()
    data_fengsu = [{'value': fengsus, 'name': '风频数'}]
    # print(data_fengsu)
    charts = Radar()
    charts.set_colors(['#4587E7'])  # 设置颜色
    charts.add_schema(schema=season_js,
                      shape='circle',
                      center=['50%', '50%'],
                      radius='80%',
                      angleaxis_opts=opts.AngleAxisOpts(
                          min_=0,  # 坐标轴刻度最小值
                          max_=360,  # 坐标轴刻度最大值
                          is_clockwise=True,
                          interval=22.5,  # 强制设置坐标轴分割间隔
                          axistick_opts=opts.AxisTickOpts(is_show=False),
                          axislabel_opts=opts.LabelOpts(is_show=False,),   # 坐标轴线标签配置项
                          axisline_opts=opts.AxisLineOpts(is_show=True),  # 坐标轴线风格配置项
                          splitline_opts=opts.SplitLineOpts(is_show=True)  # 分割线配置项
                      ),
                      radiusaxis_opts=opts.RadiusAxisOpts(
                          min_=n_min,  # 坐标轴刻度最小值
                          max_=n_max,   # 坐标轴刻度最大值
                          interval=2,  # 强制设置坐标轴分割间隔
                          splitarea_opts=opts.SplitAreaOpts(
                              is_show=True,
                              areastyle_opts=opts.AreaStyleOpts(opacity=0.2,
                                                                )
                          ),
                          splitline_opts=opts.SplitLineOpts(is_show=True,
                                                            linestyle_opts=opts.LineStyleOpts(is_show=True,
                                                                                              width=0.5,
                                                                                              color='grey')),
                          axislabel_opts=opts.LabelOpts(is_show=True,
                                                        font_size=12,
                                                        color='grey'),  # 坐标轴线标签配置项
                      ),
                      polar_opts=opts.PolarOpts(),
                      splitarea_opt=opts.SplitAreaOpts(is_show=True),
                      splitline_opt=opts.SplitLineOpts(is_show=False),  # 分割线配置项
                      textstyle_opts=opts.TextStyleOpts(color='black',
                                                        font_size=14)
                      )
    charts.add(series_name='%s玫瑰图' % season_name,  # 系列名称
               data=data_fengsu,  # 系列数据
               areastyle_opts=opts.AreaStyleOpts(opacity=0.5,  # 系列面样式设置
                                                 color=seasonareacolor),
               linestyle_opts=opts.LineStyleOpts(width=2,  # 系列线样式设置
                                                 color=seasonlinecolor),
               label_opts=opts.LabelOpts(is_show=False),
               )  # 系列标签设置
    charts.render(filechart)


if __name__=='__main__':
    '''step1 提取风向风速信息'''
    workpath = "c:\\users\\jli\\desktop\\"
    qixiangs = workpath + "qixiangs.csv"
    infos = ['V01301', 'V04295', 'V11291_701', 'V11314', 'V11315']  # 分别为站点,月分,平均风速,风频,风频(不带静风)
    df_qixiangs = pd.read_csv(qixiangs, sep=',', encoding='ANSI', index_col='V01301')
    # # print(df_qixiangs.loc[(df_qixiangs.index == 54709) & (df_qixiangs['V04295'] == 1) & (df_qixiangs['V11315'] < 999),
    # # ['V11315']])
    # # print(df_qixiangs.loc[(df_qixiangs.index == 54709) & (df_qixiangs['V04295'] == 1)]['V11315'])
    # qx_zhandians = df_qixiangs.index.to_list()  # 获取站点
    # qx_zhandiansn = list(set(qx_zhandians))  # 站点去重
    # qx_zhandiansn.sort(key=qx_zhandians.index)  # 站点重新排序与原列表保持一致
    # qx_months = [m for m in range(1, 13)]  # 设置月份
    # qx_mat = np.zeros((len(qx_zhandiansn), len(qx_months)))   # 建立多维0数组
    # df_qx_mat = pd.DataFrame(qx_mat)
    # df_qx_mat.columns, df_qx_mat.index = qx_months, qx_zhandiansn  # 为数组添加行列索引
    # # print(df_feng_mat)
    # for i in range(len(qx_zhandiansn)):  # 遍历数组行
    #     for j in qx_months:  # 遍历数组列
    #         # print(qx_zhandiansn[i], j)
    #         try:
    #             fengij = df_qixiangs.loc[(df_qixiangs.index == qx_zhandiansn[i]) & (df_qixiangs[infos[1]] == j)
    #                                      & (df_qixiangs[infos[4]] < 99999)][infos[4]].values[0]
    #             # print(fengij)
    #             df_qx_mat.iloc[i][j] = fengij
    #         except:
    #             continue
    # print(df_qx_mat)

    '''step2 构建风向风速矩阵'''
    # filefeng = "c:\\users\\jli\\desktop\\Characteristic_Code.csv"
    filefeng = "D:\\Database\\02China\\04Qixiang\\Characteristic_Code.csv"
    df_fengcodes = pd.read_csv(filefeng, sep=',', encoding='ANSI', index_col=0)
    # print(fengcodes)
    oris = df_fengcodes.index.to_list()
    codes = df_fengcodes['code']
    # print(oris)
    # print(df_qixiangs.loc[(df_qixiangs[infos[4]] == 'NW') & (df_qixiangs[infos[1]] == 1)][infos[4]].sum())
    months = [m for m in range(1, 13)]  # 设置月份
    feng_mat = np.zeros((len(oris), len(months)))  # 建立多维0数组
    df_feng_mat = pd.DataFrame(feng_mat)
    df_feng_mat.columns, df_feng_mat.index = months, oris  # 为数组添加行列索引
    # print(df_feng_mat)
    for i in months:  # 遍历数组行
        for j in range(len(oris)):  # 遍历数组列
            # print(i, oris[j], codes[j])
            try:
                # 统计i月出现j风信息,排除异常值
                fengij = df_qixiangs.loc[(df_qixiangs[infos[4]] == codes[j]) & (df_qixiangs[infos[1]] == i) &
                                         (df_qixiangs[infos[4]] < 99999)][infos[4]].to_list()
                # print(fengij, len(fengij))
                df_feng_mat.iloc[j][i] = len(fengij)
            except:
                continue
    print(df_feng_mat)

    '''step3 统计不同季节信息'''
    all_seasons = count_seasons(df_feng_mat, oris)  # 四季并列统计

    '''step4 生成风玫瑰图'''
    seasonnames = ['春季', '夏季', '秋季', '冬季', '四季']
    seasonareacolors = ['#90EE90', '#008000', '#87CEFA', '#F0FFFF', '#BC8F8F', ]  # 分割面颜色
    seasonlinecolors = ['#2E8B57', '#006400', '#4682B4', '#2F4F4F', '#800000', ]  # 分割线颜色
    for i in range(len(seasonnames)):
        filechart = workpath + seasonnames[i] + '.html'
        draw_radar(all_seasons[i], seasonnames[i], filechart, seasonareacolors[i], seasonlinecolors[i])
    print("welldone!")