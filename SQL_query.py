sql
SELECT
    ads.id AS "ad_id (Номер объявления)",
    ads.title_1 AS "title_1 (Заголовок 1)",
    ads.title_2 AS "title_2 (Заголовок 2)",
    ads.text AS "adv_text (Текст объявления)",
    SUM(costs.impressions) AS "Количество показов (impressions)",
    SUM(costs.clicks) AS "Количество кликов (clicks)",
    SUM(costs.cost) AS "Всего расход",
    SUM(CASE WHEN crm.sent_kp = 'Да' THEN 1 ELSE 0 END) AS "Всего отправлено КП",
    SUM(CASE WHEN crm.agreement = 'Да' THEN 1 ELSE 0 END) AS "Всего согласований бюджета",
    SUM(CASE WHEN crm.objections = 'Да' THEN 1 ELSE 0 END) AS "Всего работы с возражениями",
    SUM(CASE WHEN crm.project_completed = 'Да' THEN 1 ELSE 0 END) AS "Всего проект окончен / полная оплата"
FROM
    ads_direct ads
LEFT JOIN direct_cost costs ON ads.id = costs.ad_id
LEFT JOIN report_crm crm ON ads.id = crm.utm_content
WHERE
    costs.cost > 0
GROUP BY
    ads.id,
    ads.title_1,
    ads.title_2,
    ads.text;
