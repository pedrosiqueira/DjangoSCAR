# todo list
- cada porta terá um identificador. mas como a porta saberá seu identificador? a princípio, toda porta teria uma constante 'identificador' não inicializada. toda vez que uma porta ligasse, se a constante 'identificador' não estivesse inicializada, publicaria uma msg para a central, que ao receber, criaria um registro na tabela Porta do banco de dados, mas sem preencher os campos nome e descrição. assim, o admin saberia qual a porta que solicitou um identificador, pelos campos nome e descrição não preenchidos. depois que o admin manualmente desse um nome e descrição ao registro, a central publicaria uma msg para aquela porta específica, passando o identificador dela, que seria armazenado na constante 'identificador' da porta. assim, caso a porta reiniciasse, como a constante 'identificador' já estaria inicializada, ela saberia que já estaria registrada na central.

- no momento as senhas não são criptografadas

- funcao FingerPrintField, método clean, retornar fingerprint_characteristics compactada

- e como garantir que a mensagem publicada chegou? será que algum daqueles QoS do MQTT garantem a entrega?