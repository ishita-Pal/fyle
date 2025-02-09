WITH teacher_grades AS (
    SELECT teacher_id, COUNT(*) AS total_graded
    FROM assignments
    WHERE grade = 'A'
    GROUP BY teacher_id
),
max_teacher AS (
    SELECT teacher_id
    FROM teacher_grades
    ORDER BY total_graded DESC
    LIMIT 1
)
SELECT COUNT(*) AS total_a_count
FROM assignments
WHERE grade = 'A'
  AND teacher_id = (SELECT teacher_id FROM max_teacher);
