import pandas as pd

# Чтение файлов
direct_costs_df = pd.read_excel("data/direct_cost.xlsx")
report_crm_df = pd.read_excel("data/report_CRM.xlsx")
ads_direct_df = pd.read_excel("data/ads_direct.csv.xlsx")

# Очистка и стандартизация данных
ads_direct_df['ID объявления'] = ads_direct_df['ID объявления'].astype(str)
direct_costs_df['№ Объявления'] = direct_costs_df['№ Объявления'].str.replace('M-', '')
report_crm_df['utm_content.1'] = report_crm_df['utm_content.1'].str.extract(r'aid_(\d+)')[0]

# Сопоставление номеров объявлений и объединение данных
merged_df = pd.merge(ads_direct_df, direct_costs_df, left_on='ID объявления',
                     right_on='№ Объявления', how='outer')
merged_df = pd.merge(merged_df, report_crm_df, left_on='ID объявления',
                     right_on='utm_content.1', how='outer')

# Преобразование столбцов с ответами "Да"/"Нет" в числовые значения
columns_to_count = [
    'Отправлено КП',
    'Согласование бюджета',
    'Работа с возражениями',
    'Проект окончен / полная оплата'
]

for column in columns_to_count:
    merged_df[column] = merged_df[column].apply(
        lambda x: 1 if x == 'Да' else 0)

# Фильтрация по позициям, где был расход
filtered_df = merged_df[merged_df['Расход (руб.)'] > 0]

# Переименование столбцов для соответствия заданию
renamed_df = filtered_df.rename(columns={
    'ID объявления': 'ad_id (Номер объявления)',
    'Заголовок 1': 'title_1 (Заголовок 1)',
    'Заголовок 2': 'title_2 (Заголовок 2)',
    'Текст': 'adv_text (Текст объявления)',
    'Показы': 'Количество показов (impressions)',
    'Клики': 'Количество кликов (clicks)',
    'Расход (руб.)': 'Всего расход',
    'Отправлено КП': 'Всего отправлено КП',
    'Согласование бюджета': 'Всего согласований бюджета',
    'Работа с возражениями': 'Всего работы с возражениями',
    'Проект окончен / полная оплата': 'Всего проект окончен / полная оплата'
})

# Агрегация данных для расчета сумм
aggregated_df = renamed_df.groupby('ad_id (Номер объявления)').agg({
    'title_1 (Заголовок 1)': 'first',
    'title_2 (Заголовок 2)': 'first',
    'adv_text (Текст объявления)': 'first',
    'Количество показов (impressions)': 'sum',
    'Количество кликов (clicks)': 'sum',
    'Всего расход': 'sum',
    'Всего отправлено КП': 'sum',
    'Всего согласований бюджета': 'sum',
    'Всего работы с возражениями': 'sum',
    'Всего проект окончен / полная оплата': 'sum'
}).reset_index()

# Сохранение в новый файл
aggregated_df.to_excel("final_report.xlsx", index=False)
