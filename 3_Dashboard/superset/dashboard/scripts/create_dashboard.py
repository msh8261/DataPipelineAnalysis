from supersetapi import SupersetAPIClient
import os 

postgres_password = os.environ.get('POSTGRES_PASSWORD')

client = SupersetAPIClient(host="http://172.18.0.6:8088")
client.login(username="admin", password="admin")

# Connect Superset to Postgres DB
database_id = client.create_database(
    database_name="PostgreSQL", 
    engine="postgresql", 
    driver="psycopg2",
    sqlalchemy_uri=f"postgresql://postgres:{postgres_password}@host.docker.internal:5432/dvd_rentals"
)#postgresql+psycopg2

dataset_id = client.create_dataset(
    database_id=database_id,
    schema="public",
    table="category_recommendations_ranked"
)

dashboard_id = client.create_dashboard(title="DVD Rentals Dashboard")


# Create Pie Chart
params = "{\"groupby\":[\"category_name\"],\
            \"metric\":{\"expressionType\":\"SIMPLE\",\
            \"column\":{\"column_name\":\"category_rank\",\
            \"filterable\":true,\
            \"groupby\":true},\
            \"aggregate\":\"SUM\",\
            \"label\":\"SUM(customer_id)\"},\
            \"color_scheme\":\"supersetColors\",\
            \"show_labels_threshold\":5,\
            \"show_legend\":true,\
            \"legendType\":\"scroll\",\
            \"legendOrientation\":\"top\",\
            \"label_type\":\"key\",\
            \"number_format\":\"SMART_NUMBER\",\
            \"show_labels\":true,\
            \"labels_outside\":true,\
            \"outerRadius\":70,\
            \"innerRadius\":30\
        }"

total_sales_chart = client.create_chart(
    dashboard_ids=[dashboard_id], 
    datasource_id=dataset_id, 
    datasource_name="dvd_rentals.category_recommendations_ranked",
    params=params,
    slice_name="Category Name",
    viz_type="pie"
)


# # Create Bar Chart
params = "{\"metrics\":[{\"expressionType\":\"SIMPLE\",\
            \"column\":{\"column_name\":\"category_rank\",\
            \"filterable\":true,\
            \"groupby\":true,\
            \"id\":4,\
            \"type\":\"FLOAT\"},\
            \"aggregate\":\"SUM\",\
            \"label\":\"SUM(film_id)\"}],\
            \"groupby\":[\"category_rank\"],\
            \"columns\":[],\
            \"row_limit\":10000,\
            \"timeseries_limit_metric\":{\"expressionType\":\"SIMPLE\",\
            \"column\":{\"column_name\":\"rental_counts\",\
            \"filterable\":true,\
            \"groupby\":true,\
            \"id\":4,\
            \"type\":\"FLOAT\"},\
            \"aggregate\":\"SUM\",\
            \"label\":\"SUM(film_id)\"},\
            \"order_desc\":true,\
            \"color_scheme\":\"supersetColors\",\
            \"show_legend\":true,\
            \"show_bar_value\":true,\
            \"rich_tooltip\":true,\
            \"order_bars\":false,\
            \"y_axis_format\":\"SMART_NUMBER\",\
            \"y_axis_bounds\":[null,null],\
            \"bottom_margin\":\"auto\",\
            \"x_ticks_layout\":\"auto\"\
        }"

total_sales_chart = client.create_chart(
    dashboard_ids=[dashboard_id], 
    datasource_id=dataset_id, 
    datasource_name="dvd_rentals.category_recommendations_ranked",
    params=params,
    slice_name="Category Rnak, Rental Count",
    viz_type="dist_bar"
)

print("Superset Dashboard created successfully...")