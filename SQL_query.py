sql
CREATE VIEW ads_report AS
SELECT
    ads_direct.ad_id,
    ads_direct.title_1,
    ads_direct.title_2,
    ads_direct.adv_text,
    SUM(direct_cost.impressions) as impressions,
    SUM(direct_cost.clicks) as clicks,
    SUM(direct_cost.total_cost) as total_cost,
    SUM(report_CRM.total_sent) as total_sent,
    SUM(report_CRM.total_agreed) as total_agreed,
    SUM(report_CRM.total_objections) as total_objections,
    SUM(report_CRM.total_finished) as total_finished
FROM
    direct_cost
    INNER JOIN report_CRM ON direct_cost.ad_id = report_CRM.ad_id
    INNER JOIN ads_direct ON direct_cost.ad_id = ads_direct.ad_id
WHERE
    direct_cost.total_cost > 0
GROUP BY
    ads_direct.ad_id;
