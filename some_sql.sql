-- 一些SQL统计脚本

--- 按天统计省份及通道，分开不同登陆比
select t1.d 日期, t1.sp_type, t1.channel,  t3.cnt totalCnt,
if(t1.cnt/t3.cnt >= 0.05, concat( '>5% ',t1.sp_type, ' ** ', t1.cnt/t3.cnt), t1.cnt/t3.cnt)通道占比,
t1.cnt tryCnt, t2.cnt sucCnt,
if(t2.cnt/t1.cnt <= 0.8, concat(t2.cnt/t1.cnt, ' ** ' ,t1.sp_type), '') '登陆比小于80%',
if(t2.cnt/t1.cnt > 0.8, t2.cnt/t1.cnt, '') '登陆比大于80%'
from (select date_format(created_time, '%Y-%m-%d') d, sp_type, channel, count(distinct phone)cnt
from authuser
where created_time > date_sub(curdate(), interval 1 day)
group by d, sp_type, channel
)t1 left join
(select date_format(created_time, '%Y-%m-%d') d, sp_type, channel, count(distinct phone) cnt
from authuser
where created_time > date_sub(curdate(), interval 1 day)
and status > 0
group by d, sp_type, channel
)t2 on t1.d=t2.d and t1.sp_type=t2.sp_type and t1.channel=t2.channel left join
(select date_format(created_time, '%Y-%m-%d')d, count(distinct phone)cnt
from authuser
where created_time > date_sub(curdate(), interval 1 day)
group by d
)t3 on t1.d=t3.d;
-- 按小时统计当天登陆比
select t1.d 日期, t1.sp_type, t1.channel,  t3.cnt totalCnt, t1.cnt/t3.cnt 通道占比,
t1.cnt tryCnt, t2.cnt sucCnt,
if(t2.cnt/t1.cnt <= 0.8, t2.cnt/t1.cnt, '') '小于80%',
if(t2.cnt/t1.cnt > 0.8, t2.cnt/t1.cnt, '') '大于80%'
from (select date_format(created_time, '%Y-%m-%d %H') d, sp_type, channel, count(distinct phone)cnt
from authuser
where created_time > date_sub(curdate(), interval 0 day)
group by sp_type, channel, d
)t1 left join
(select date_format(created_time, '%Y-%m-%d %H') d, sp_type, channel, count(distinct phone) cnt
from authuser
where created_time > date_sub(curdate(), interval 0 day)
and status > 0
group by sp_type, channel, d
)t2 on t1.d=t2.d and t1.sp_type=t2.sp_type and t1.channel=t2.channel left join
(select date_format(created_time, '%Y-%m-%d %H')d, count(distinct phone)cnt
from authuser
where created_time > date_sub(curdate(), interval 0 day)
group by d
)t3 on t1.d=t3.d;

SELECT t1.d 按天统计, t1.supplier 运营商, t3.cnt 魔蝎请求用户, t4.cnt 魔蝎成功, t1.cnt amsu请求用户, t2.cnt amsu成功数,
t4.cnt/t3.cnt 魔蝎登陆比, t2.cnt/t1.cnt amsu登陆比,  (t4.cnt/t3.cnt-t2.cnt/t1.cnt)差值 from
(SELECT  DATE_FORMAT(created_at,'%Y-%m-%d') d, count(DISTINCT phone)cnt, supplier from _spauthtask
	where  created_at > DATE_SUB(CURDATE(),INTERVAL 6 DAY)  and  sp_type = 4  and supplier = '移动'
	and auth_type=2 and status != 0
	group by d, supplier
)t1 LEFT JOIN
(SELECT  DATE_FORMAT(created_at,'%Y-%m-%d') d, COUNT(DISTINCT phone)cnt, supplier from _spauthtask
	where  created_at > DATE_SUB(CURDATE(),INTERVAL 6 DAY)  and sp_type = 4  and status in (100, 101, 70)
	and auth_type=2
	group by d, supplier
)t2 on t1.d=t2.d and t1.supplier=t2.supplier left join
(SELECT  DATE_FORMAT(created_at,'%Y-%m-%d') d, count(DISTINCT phone)cnt, supplier from _spauthtask
	where  created_at > DATE_SUB(CURDATE(),INTERVAL 6 DAY)  and  sp_type = 2  and supplier = '移动'
	and auth_type=2 and status != 0
	group by d, supplier
)t3 on t3.d=t2.d and t3.supplier=t2.supplier LEFT JOIN
(SELECT  DATE_FORMAT(created_at,'%Y-%m-%d') d, COUNT(DISTINCT phone)cnt, supplier from _spauthtask
	where  created_at > DATE_SUB(CURDATE(),INTERVAL 6 DAY)  and sp_type = 2  and status in (100, 101, 70)  and supplier='移动'
	and auth_type=2
	group by d, supplier
)t4 on t3.d=t4.d and t3.supplier=t4.supplier;