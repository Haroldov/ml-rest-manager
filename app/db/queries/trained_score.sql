WITH ranked_models AS (
     SELECT model_id,
     	    model_type,
	    num_training,
	    ROW_NUMBER() OVER (PARTITION BY model_type ORDER BY model_type, num_training ASC) AS rn
     FROM ml_metadata
),
max_ranked_models AS (
     SELECT model_type, MAX(num_training) AS max_per_type, MAX(rn) AS max_rn
     FROM ranked_models
     GROUP BY model_type
)
SELECT *,
       CASE max_rn WHEN 1 THEN 1 ELSE
        (rn - 1) / (max_rn - 1)
       END AS trained_score
FROM ranked_models m
INNER JOIN max_ranked_models s ON s.model_type = m.model_type
ORDER BY s.model_type, num_training DESC, rn DESC
