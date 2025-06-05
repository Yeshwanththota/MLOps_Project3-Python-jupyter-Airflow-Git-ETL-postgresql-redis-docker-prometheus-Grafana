FROM quay.io/astronomer/astro-runtime:12.6.0

RUN pip install apache-airflow-providers-google
# RUN pip install "astro-sdk-python>=1.6.0"