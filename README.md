# Airbnb Reviews Analysis

Este projeto utiliza Streamlit para análise de dados de hospedagens e reviews do Airbnb.

## Configuração do ambiente

### Usando Conda

1. Instale o [Miniconda](https://docs.conda.io/en/latest/miniconda.html) ou [Anaconda](https://www.anaconda.com/products/distribution).
2. Crie um arquivo `environment.yml` com o seguinte conteúdo:
   ```sh
   name: data-analysis-env
   channels:
      - conda-forge
   dependencies:
      - python=3.13
      - streamlit=1.48.1
      - pandas
      - numpy
      - plotly
      - pillow
   ```
3. Crie o ambiente com o arquivo `environment.yml`:

   ```sh
   conda env create -f environment.yml
   ```

4. Ative o ambiente:

   ```sh
   conda activate data-analysis-env
   ```

### Usando venv + pip

1. Instale o Python (recomendado 3.13).
2. Crie e ative o ambiente virtual:

   ```sh
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   .venv\Scripts\activate     # Windows
   ```

3. Crie um arquivo `requirements.txt` com o seguinte conteúdo:

   ```sh
   streamlit==1.48.1
   pandas==2.3.2
   numpy==2.3.2
   plotly==6.3.0
   ```

1. Instale as dependências:

   ```sh
   pip install -r requirements.txt
   ```

## Executando o projeto

Para iniciar o aplicativo Streamlit, execute:

```sh
streamlit run app.py
```

O app estará disponível em `http://localhost:8501`.

## Estrutura

- `app.py`: Código principal do aplicativo Streamlit.
- `requirements.txt`: Dependências para uso com pip/venv.
- `environment.yml`: Dependências para uso com conda.
- `data/*`: Dados estáticos do projeto (e.g. imagens, datasets).
- `pages/*`: Páginas que podem ser acessadas na aplicação.

## Aplicação publicada

Para acessar a aplicação na web, acesse: https://airbnb-reviews-analysis-viz.streamlit.app/