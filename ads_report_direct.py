import pandas as pd

# Загрузка данных из файлов
direct_cost = pd.read_excel('data/direct_cost.xlsx')
report_CRM = pd.read_excel('data/report_CRM.xlsx')
ads_direct = pd.read_excel('data/ads_direct.csv.xlsx')

# Посмотрим, какие колонки есть в каждом из датафреймов
print(direct_cost.columns)
print(report_CRM.columns)
print(ads_direct.columns)

# Объединение данных
merged = direct_cost.merge(report_CRM, on='ad_id').merge(ads_direct, on='ad_id')

# Фильтрация данных (только те объявления, на которые были потрачены деньги)
filtered = merged[merged['total_cost'] > 0]

# Подсчет необходимых параметров
ads_report = filtered.groupby('ad_id').agg({
    'title_1': 'first',
    'title_2': 'first',
    'adv_text': 'first',
    'impressions': 'sum',
    'clicks': 'sum',
    'total_cost': 'sum',
    'total_sent_CP': 'sum',
    'total_agreed_budget': 'sum',
    'total_objections': 'sum',
    'total_finished_project': 'sum'
})

# Вывод отчета
print(ads_report)
