# Controle de Volume e Mídia com Gestos

Este projeto utiliza a webcam e o MediaPipe para detectar gestos da mão e controlar o volume do sistema, além de permitir a pausa e retomada da reprodução de mídia.

## Recursos
- **Controle de Volume:** Ajuste o volume do sistema aproximando ou afastando o polegar e o indicador.
- **Pausa e Reprodução de Mídia:** Faça um gesto de "pinça" cinco vezes para alternar entre pausar e retomar a reprodução de mídia.
- **Ativação e Desativação da Captura:** Pressione "5" para ativar ou desativar a captura de gestos.

## Requisitos

Certifique-se de ter os seguintes pacotes instalados:

```sh
pip install opencv-python mediapipe pycaw comtypes
```

## Como Usar

1. Execute o script Python.
2. Pressione **5** para ativar a captura de gestos.
3. Para **ajustar o volume**:
   - Aproxime o polegar e o indicador para **diminuir o volume**.
   - Afaste o polegar e o indicador para **aumentar o volume**.
4. Para **pausar/retomar a reprodução**, faça o gesto de pinça 5 vezes.
5. Pressione **q** para sair.

## Funcionamento
- O script usa **MediaPipe** para detectar a mão na webcam.
- Calcula a distância entre o polegar e o indicador para determinar os comandos.
- Utiliza **pycaw** para manipular o volume do sistema.
- Simula um pressionamento de tecla para controlar a reprodução de mídia.

## Contribuição
Fique à vontade para contribuir com melhorias ou otimizações. Caso encontre bugs, abra uma issue.

