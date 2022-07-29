{% macro unpack_json(field_name,column_name = 'event_properties') %}
    (nullif(json_extract_path_text({{column_name}},'{{field_name}}',true),null))
{% endmacro %}
{% macro unpack_json_no_null(field_name,column_name = 'event_properties') %}
    (nullif(json_extract_path_text({{column_name}},'{{field_name}}',true),'') :: FLOAT)
{% endmacro %}
