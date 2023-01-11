SELECT model_id,
       s.model_type,
       num_training,
       CASE max_rn WHEN 1 THEN 1 ELSE
        (rn - 1) / (max_rn - 1)
       END AS trained_score
FROM (
    SELECT *, IF(@prev <> model_type, @rn:=0,@rn), @prev:=model_type, @rn:=@rn+1 AS rn
    FROM db.ml_metadata, (SELECT @rn:=0)rn, (SELECT @prev:='')prev
    ORDER BY model_type, num_training ASC
    ) m
INNER JOIN (
    SELECT model_type, MAX(num_training) as max_per_type, MAX(rn) as max_rn FROM (
        (
    SELECT *, IF(@prev <> model_type, @rn:=0,@rn), @prev:=model_type, @rn:=@rn+1 AS rn
    FROM db.ml_metadata, (SELECT @rn:=0)rn, (SELECT @prev:='')prev
    ORDER BY model_type, num_training ASC
    ) m                                                       )
    GROUP BY model_type
) s ON s.model_type = m.model_type
ORDER BY s.model_type, num_training DESC, rn DESC
