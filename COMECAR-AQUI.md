# InVet Center — dashboard, estado atual

Dashboard de performance da **InVet Center Limeira · Hospital Veterinário 24h**, feito a partir do
modelo em `Nohotel`. O passo a passo genérico, com os erros conhecidos, está em
[`PLAYBOOK-NOVO-CLIENTE.md`](PLAYBOOK-NOVO-CLIENTE.md).

## Já está pronto

- **Google Ads coletado e funcionando.** Conta `182-911-9223`
  (*InVet Center Limeira Hospital Veterinário 24h*), via MCC `295-287-1856`.
  Série diária de **01/01/2025 a 20/09/2026**: 543 dias, 6 campanhas, 15 grupos,
  R$ 18.267 investidos e 6.211 contatos.
- **Metas tiradas do histórico real** (não inventadas): R$ 2,80 por contato — mediana mensal
  de R$ 2,82, melhor mês R$ 2,29, últimos 90 dias R$ 2,76. Verba Google R$ 1.250/mês
  (média de R$ 1.234 nos últimos 6 meses fechados). A origem de cada número está
  em `_comentario_metas`, dentro de `public/config.json`.
- **Meta Ads zerado de propósito.** Não trabalhamos Meta Ads para esse cliente hoje. O
  `scripts/meta_zerado.py` gera `meta.json` e `organic.json` no mesmo formato do coletor real,
  com tudo em zero — as páginas de Meta Ads aparecem no menu e mostram R$ 0,00 e 0 contatos,
  ao lado do Google Ads com resultado. Nenhum texto aponta isso: o contraste fala por si.
- **Vocabulário adaptado ao cliente.** O modelo era de hotel e falava "reservas" e "carrinhos".
  Agora fala **contato**, **ligação** e **conversa no WhatsApp**, que é o funil de um
  pronto-socorro veterinário. Ligações saem da categoria `PHONE_CALL_LEAD` do Google Ads
  (1.285 no histórico) e contatos de site/WhatsApp da categoria `CONTACT` (4.926).
- **Receita e ROAS desligados** em `config.json` → `display.revenue`. O valor que vem em
  `conversions_value` do Google Ads é o peso interno da conversão na conta, não faturamento:
  exibir como receita gerava um ROAS falso de 0,05×.
- **Camada de senha**: 32/32 testes passando. Senha e chave de sessão em `SENHA-LOCAL.txt`
  (fora do git).
- **Pacote de deploy** montado em `deploy-netlify/` (15 arquivos, 1,1 MB).

## Falta fazer

1. **Trocar a logo.** `public/logo.jpg` ainda é a do Nohotel — aparece no menu lateral.
   Substitua por uma logo quadrada da InVet Center, 150px ou mais, e rode `npm run bundle` de novo.
2. **Criar o site no Netlify**: *Add new site → Deploy manually* → arraste a pasta
   **`deploy-netlify`** (não a `public/`, senão o site sobe sem senha).
3. **Cadastrar a senha** em *Site configuration → Environment variables*, escopo **All scopes**,
   **sem** marcar "Contains secret values" (se marcar, a Edge Function não recebe o valor e o site
   responde 503 em tudo): `DASHBOARD_PASSWORD` e `SESSION_SECRET`, os dois em `SENHA-LOCAL.txt`.
   Depois **publique de novo** — variável nova só vale no deploy seguinte.
4. **Cadastrar os secrets no GitHub** (*Settings → Secrets and variables → Actions*).
   `SEGREDOS-GITHUB.txt` já tem 6 prontos para copiar; faltam os dois do Netlify:
   `NETLIFY_AUTH_TOKEN` (Netlify → User settings → Applications → Personal access tokens) e
   `NETLIFY_SITE_ID` (Site configuration → Site details, depois de criar o site).
5. **Rodar o workflow** em *Actions → Atualizar dashboard → Run workflow* e conferir que termina
   verde. Ele roda os testes de senha antes de publicar e confere na URL que `/data/*.json`
   responde 401 sem sessão — se a proteção não subir, o job falha em vez de deixar os dados abertos.

## Quando o Meta Ads entrar

Não precisa mexer em código. Cadastre a **variável** (não secret) `META_AD_ACCOUNT_ID` no
repositório, em *Settings → Secrets and variables → Actions → Variables*, e o workflow passa a
rodar `scripts/fetch_meta.py` em vez do gerador zerado. Também vale preencher `META_PAGE_ID` e
`META_IG_USER_ID` (para o orgânico) e os IDs em `public/config.json`. Antes disso, dê acesso ao
**Usuário do Sistema** do Meta na conta de anúncios, na página e no Instagram do cliente — é o
erro mais comum, e o playbook §4 mostra como conferir.

Na mesma hora, revise a meta de custo por contato do Meta: os R$ 2,80 vêm de busca (intenção),
e descoberta normalmente custa mais. Deixar os R$ 2,80 valendo para o Meta deixaria tudo vermelho.

## Comandos

```bash
npm test                        # 32 verificações da camada de senha
python scripts/fetch_google.py  # recoleta o Google Ads (lê .env.google)
python scripts/meta_zerado.py   # regera meta.json e organic.json zerados
npm run bundle                  # monta deploy-netlify/ para subir no Netlify
npm run dev                     # http://localhost:8790 (com a senha local)
```

## Repositório

```bash
git remote -v   # origin → InVet-Center-Steink-Performance-Dashboard
```

Os dados (`public/data/*.json`), os segredos (`.env*`) e a senha (`SENHA-LOCAL.txt`) estão no
`.gitignore` e nunca vão para o git — o repositório é público. Os JSONs são gerados na hora do
deploy e enviados direto para o Netlify.
