$(document).ready(function() {
  // Aplicar máscara de telefone
  $('#inputTEL').mask('(00)00000-0000');

  // Aplicar máscara de CPF
  $('#inputCPF').mask('000.000.000-00', {reverse: true});
});

