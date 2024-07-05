DROP TABLE IF EXISTS category_recommendations_ranked;
CREATE TABLE category_recommendations_ranked as
with complete_joint_dataset AS(
    SELECT
        rental.customer_id,
        inventory.film_id,
        film.title,
        category.name AS category_name,
        rental.rental_date
    FROM
        rental
        INNER JOIN inventory ON rental.inventory_id = inventory.inventory_id
        INNER JOIN film ON inventory.film_id = film.film_id
        INNER JOIN film_category ON film.film_id = film_category.film_id
        INNER JOIN category ON film_category.category_id = category.category_id
),
category_counts as (
    select
        customer_id,
        category_name,
        count(*) as rental_count,
        max(rental_date) as latest_rental_date
    from
        complete_joint_dataset
    group by
        customer_id,
        category_name
),
top_categories as (
    select
        customer_id,
        category_name,
        rental_count,
        latest_rental_date,
        DENSE_RANK() over(
            partition by customer_id
            order by
                rental_count desc,
                latest_rental_date desc,
                category_name
        ) as category_rank
    from
        category_counts
),
film_counts as (
    select
        distinct film_id,
        title,
        category_name,
        count(*) over(partition by film_id) as rental_counts
    from
        complete_joint_dataset
),
category_film_exclusions as (
    select
        film_id,
        customer_id
    from
        complete_joint_dataset
),
category_recommendations as (
    select
        tc.customer_id,
        tc.category_name,
        tc.category_rank,
        fc.film_id,
        fc.title,
        fc.rental_counts,
        DENSE_RANK() over(
            partition by tc.customer_id,
            tc.category_rank
            order by
                fc.rental_counts desc,
                fc.title
        ) as reco_rank
    from
        top_categories as tc
        inner join film_counts as fc on tc.category_name = fc.category_name
    WHERE
        NOT EXISTS (
            SELECT
                1
            FROM
                category_film_exclusions
            WHERE
                category_film_exclusions.customer_id = tc.customer_id
                AND category_film_exclusions.film_id = fc.film_id
        )
)
select
    *
from
    category_recommendations
where
    reco_rank <= 3;