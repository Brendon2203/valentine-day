# Valentine's Day App

Um aplicativo web para criar pedidos de namoro personalizados com fotos, mensagens e músicas do Spotify.

## Configuração para Deploy na Vercel

1. Primeiro, crie uma conta no [Cloudinary](https://cloudinary.com/) (gratuito) para armazenar as imagens.

2. Configure as seguintes variáveis de ambiente no painel da Vercel:

   - `CLOUDINARY_CLOUD_NAME`: Seu cloud name do Cloudinary
   - `CLOUDINARY_API_KEY`: Sua API key do Cloudinary
   - `CLOUDINARY_API_SECRET`: Seu API secret do Cloudinary
   - `FLASK_ENV`: Defina como "production"
   - `FLASK_APP`: Defina como "api/index.py"

3. Conecte seu repositório GitHub à Vercel:
   - Faça login na [Vercel](https://vercel.com)
   - Clique em "New Project"
   - Importe seu repositório do GitHub
   - Configure as variáveis de ambiente mencionadas acima
   - Clique em "Deploy"

## Desenvolvimento Local

1. Clone o repositório:

```bash
git clone <seu-repositorio>
cd valentine-day
```

2. Crie um arquivo `.env` na raiz do projeto com as variáveis de ambiente necessárias (veja `.env.example`).

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Execute o servidor de desenvolvimento:

```bash
flask run
```

## Tecnologias Utilizadas

- Flask (Backend)
- TailwindCSS (Estilização)
- Cloudinary (Armazenamento de imagens)
- Vercel (Hospedagem)
