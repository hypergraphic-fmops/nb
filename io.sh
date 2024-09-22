#!/bin/bash

# Verifica se um argumento foi fornecido
if [ -z "$1" ]; then
  echo "Uso: $0 <diretorio>"
  exit 1
fi

# Lista os arquivos no diretório
ls "$1"