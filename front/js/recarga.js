// Endereço da API. Se a porta ou o endereço mudarem, ajuste só aqui.
const API_URL = "http://localhost:8000";

const campoCartao = document.getElementById("cartaoId");
const campoValor = document.getElementById("valor");
const blocoDados = document.getElementById("dadosCartao");
const blocoRecarga = document.getElementById("areaRecarga");
const textoNome = document.getElementById("nome");
const textoSaldo = document.getElementById("saldo");
const textoStatus = document.getElementById("status");
const mensagem = document.getElementById("mensagem");

// Transforma 14.6 em "R$ 14,60".
function moeda(valor) {
    return valor.toLocaleString("pt-BR", { style: "currency", currency: "BRL" });
}

function mostrarMensagem(texto, tipo) {
    mensagem.textContent = texto;
    mensagem.className = "mensagem " + tipo;
    mensagem.hidden = false;
}

function esconderCartao() {
    blocoDados.hidden = true;
    blocoRecarga.hidden = true;
}

// Pergunta à API quem é o cartão e quanto tem de saldo.
async function consultar() {
    const id = campoCartao.value;
    if (!id) {
    mostrarMensagem("Digite o número do cartão.", "erro");
    return;
    }

    try {
    const resposta = await fetch(`${API_URL}/cartoes/${id}`);

    if (resposta.status === 404) {
        esconderCartao();
        mostrarMensagem("Cartão não encontrado.", "erro");
        return;
    }
    if (!resposta.ok) {
        throw new Error("Resposta inesperada da API");
    }

    const dados = await resposta.json();
    textoNome.textContent = dados.nome;
    textoSaldo.textContent = moeda(dados.saldo);
    textoStatus.textContent = dados.status;
    blocoDados.hidden = false;
    blocoRecarga.hidden = false;
    mensagem.hidden = true;
    } catch (erro) {
    esconderCartao();
    mostrarMensagem("Não foi possível falar com a API. Ela está rodando?", "erro");
    }
}

// Pede à API para somar o valor ao saldo do cartão.
async function recarregar() {
    const id = campoCartao.value;
    const valor = parseFloat(campoValor.value);

    if (!valor || valor <= 0) {
    mostrarMensagem("Digite um valor maior que zero.", "erro");
    return;
    }

    try {
    const resposta = await fetch(`${API_URL}/cartoes/${id}/recarga`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ valor: valor }),
    });

    if (resposta.status === 404) {
        mostrarMensagem("Cartão não encontrado.", "erro");
        return;
    }
    if (resposta.status === 422) {
        mostrarMensagem("Valor inválido. Use um valor positivo com até duas casas decimais.", "erro");
        return;
    }
    if (!resposta.ok) {
        throw new Error("Resposta inesperada da API");
    }

    const dados = await resposta.json();
    textoSaldo.textContent = moeda(dados.saldo_atual);
    campoValor.value = "";
    mostrarMensagem(`Recarga de ${moeda(dados.valor_recarregado)} realizada com sucesso.`, "sucesso");
    } catch (erro) {
    mostrarMensagem("Não foi possível falar com a API. Ela está rodando?", "erro");
    }
}

document.getElementById("btnConsultar").addEventListener("click", consultar);
document.getElementById("btnRecarregar").addEventListener("click", recarregar);