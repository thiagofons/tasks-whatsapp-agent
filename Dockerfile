###################
# BUILD FOR LOCAL DEVELOPMENT
###################

FROM node:18-alpine As development

# Define o diretório de trabalho para a API
WORKDIR /usr/src/app/api

# Copia os arquivos package.json e package-lock.json para o container
COPY --chown=node:node api/package*.json ./

# Instala as dependências
RUN npm ci

# Copia todo o código da API para o container
COPY --chown=node:node api ./

# Garante que o diretório dist exista e tenha as permissões corretas
RUN mkdir -p /usr/src/app/api/dist && chown -R node:node /usr/src/app/api/dist

# Usa o usuário node (evita rodar como root)
USER node

###################
# BUILD FOR PRODUCTION
###################

FROM node:18-alpine As build

WORKDIR /usr/src/app/api

COPY --chown=node:node api/package*.json ./
COPY --chown=node:node --from=development /usr/src/app/api/node_modules ./node_modules
COPY --chown=node:node api ./

# Generate Prisma database client code
RUN npm run prisma:generate

# Garante que o diretório dist exista e tenha as permissões corretas
RUN mkdir -p /usr/src/app/api/dist && chown -R node:node /usr/src/app/api/dist

# Compila a aplicação
RUN npm run build

# Define a variável de ambiente para produção
ENV NODE_ENV production

# Remove dependências desnecessárias
RUN npm ci --only=production && npm cache clean --force

USER node

###################
# PRODUCTION
###################

FROM node:18-alpine As production

WORKDIR /usr/src/app/api

COPY --chown=node:node --from=build /usr/src/app/api/node_modules ./node_modules
COPY --chown=node:node --from=build /usr/src/app/api/dist ./dist

# Comando para rodar a aplicação em produção
CMD [ "node", "dist/main.js" ]
