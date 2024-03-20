<script setup>

    import 'primevue/resources/themes/aura-light-green/theme.css'
    const {data: conversas} = await useFetch('http://localhost:8000/conversationHistory/')
    const {data: conversaHistoria} = await useFetch('http://localhost:8000/conversas/')

    let response = ref("")
    const dialog = reactive({
        text: '',
        type: '',
        name: '',
        image: '',
        historyId: null
    });

    const includeDialog = ((type)=>{
        if(type === 'Q'){
            dialog.image = 'user.png';
            dialog.name = 'Usuário';            
            dialog.type = 'right';
        } else {
            dialog.image = 'bot.png';
            dialog.name = 'Bot';            
            dialog.type = 'left';
        }
        // faz a cópia profunda da estrutura com os valores atuais (deep copy)
        conversationHistory.value.push(
            JSON.parse(JSON.stringify(dialog))
        );            
    });
    
    const sendMessage = async (idConversa) => {
        
        
        if(!idConversa){
            idConversa = dialog.historyId
            includeDialog('Q');
        }else{
            dialog.historyId = idConversa
            includeDialog('Q');
        }
        
        //message.value;
        const {data: answer} = await useFetch('http://localhost:8000/chatbot/',{
            method: 'POST',
            body:{
                question: dialog.text,
                userId: 1,
                conversationId: idConversa
            }   
        })
        dialog.text = answer.value.message
        dialog.historyId = answer.value.history.id
        includeDialog('A');
        dialog.text = ''

    }

//armazena em tela o histórico das mensagens
const conversationHistory = ref([])
const conversaSelecionada = ref("")

const selecionarConversa = (idConversa) =>{
    conversaSelecionada.value = idConversa
    console.log("CONV", conversaSelecionada.value)

    conversationHistory.value = conversaHistoria.value.filter(item => item.history.id === idConversa)
    return conversationHistory.value
}

function getSeverity(conversaId) {
  return conversaSelecionada.value === conversaId ? 'primary' : 'secondary';
}


const novaConversaStatus = ref(null)
const novaConversa = async () =>{

    conversaSelecionada.value = null
    conversationHistory.value = []

    dialog.text = 'Oi'
    includeDialog('Q');
    novaConversaStatus.value = true

    const {data: answer} = await useFetch('http://localhost:8000/chatbot/',{
            method: 'POST',
            body:{
                question: dialog.text,
                userId: 1,
                conversationId: dialog.historyId
            }   
        })
        
        dialog.text = answer.value.message
        dialog.historyId = answer.value.history.id
        includeDialog('A');
        dialog.text = ''
    
    const {data: conversasNovas} = await useFetch('http://localhost:8000/conversationHistory/')
    conversas.value = conversasNovas._rawValue
}


</script>

<template>
    <div style="display: flex;">
        <div class="menu-lateral">
            <div class="titulo">
                <h2 style="color: white">CHATLGPT</h2>
                <div style="padding-left: 15px; padding-right: 15px;">
                    <Divider />
                </div>
                <Button label="Nova Conversa" severity="info" raised @click="novaConversa" />
                <div style="padding-left: 15px; padding-right: 15px;">
                    <Divider />
                </div>
            </div>
            <div v-for="conversa in conversas" :key="conversa">
                <div>
                    <Button :label="'CHAT #' + conversa.id" :severity="getSeverity(conversa.id)" raised @click="selecionarConversa(conversa.id)" />
                    <br><br>
                </div>
                
            </div>
            

        </div>
        <div class="menu-conversa">
            <div class="titulo-conversa">
                <h2 style="color: rgb(76, 76, 255)">CONVERSA</h2>
            </div>
            <Divider />
            <div class="campoConversa">
                <div v-if="conversaSelecionada">
                    <div v-for="conversation in conversationHistory" :key="conversation" style="margin: 10px">
                        <TextBox :name="conversation.history.user.username ?  conversation.name" :avatarImage="conversation.type === 'Q' ? 'user.png' : 'bot.png'" 
                            :message="conversation.message" :type="conversation.type"/> 
                            <br>
                    </div>
                </div>
                
                <div v-else>
                    <div class="box" v-for="(conversation, id) in conversationHistory" :key="id">
                        <TextBox :name="conversation.name" :avatarImage="conversation.image" 
                            :message="conversation.text" :type="conversation.type"/>  
                    </div>
                </div>  
            </div>
            <Divider />

            <div v-if="novaConversaStatus" class="campoPergunta">
                <div style="display: flex;">
                    <InputText type="text" v-model="dialog.text" style="margin-right: 10px; margin-left: 5px; width: 700px;" @keyup.enter="sendMessage(null)"/>
                    <Button @click="sendMessage(null)" label="Enviar"></Button> 
                </div>
            </div>

            <div v-if="conversaSelecionada">
                <div style="display: flex;">
                    <InputText type="text" v-model="dialog.text" style="margin-right: 10px; margin-left: 5px; width: 700px;" @keyup.enter="sendMessage(conversaSelecionada)"/>
                    <Button @click="sendMessage(conversaSelecionada)" label="Send"></Button> 
                </div>
            </div>
            
        </div>
         
    </div>
    
</template>

<style scoped>
    .campoConversa{
        height: 80vh;
        overflow-y: auto;
    }

    .campoPergunta{
        align-items: center;
        justify-content: center;
        text-align: center;
        width: 100wh;
    }
    .menu-lateral{
        background-color: rgb(76, 76, 255);
        width: 250px; 
        height: 100vh;
        text-align: center;
        overflow-y: auto;
    }

    .titulo{
        text-align: center; 
    }

    .menu-conversa{
        width: 800px;
        background-color: #fff;
        height: 100vh;
    } 

    .titulo-conversa{
        width: 100wh;
        align-items: center;
        justify-items: center;
        text-align: center;
    }
    
    .box{
        padding: 15px;
    }
</style>