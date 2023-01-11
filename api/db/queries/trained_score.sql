SELECT model_id,
       s.model_type,
       num_training,
       num_training / max_per_type AS trained_score
FROM db.ml_metadata m
INNER JOIN (
    SELECT model_type, MAX(num_training) as max_per_type FROM db.ml_metadata
    GROUP BY model_type
) s ON s.model_type = m.model_type
ORDER BY s.model_type, trained_score DESC
