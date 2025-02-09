SELECT grade, COUNT(*) AS count
FROM assignments
WHERE state = 'GRADED'
GROUP BY grade