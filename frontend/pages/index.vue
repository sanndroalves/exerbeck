<script setup>

    import 'primevue/resources/themes/aura-light-green/theme.css'

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
    
    const sendMessage = async () => {
        console.log(dialog.text);
        includeDialog('Q');
        
        //message.value;
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
    }

//armazena em tela o histórico das mensagens
const conversationHistory = ref([])
const ultimaId = ref()
</script>

<template>
    <div style="display: flex;">
        <div class="menu-lateral">
            <div class="titulo">
                <h2 style="color: white">CHATLGPT</h2>
                <div style="padding-left: 15px; padding-right: 15px;">
                    <Divider />
                </div>
                <Button label="Nova Conversa" severity="info" raised />
                <div style="padding-left: 15px; padding-right: 15px;">
                    <Divider />
                </div>
            </div>
            <div v-for="conversa in conversationHistory">
                <div v-if="conversa.historyId !== ultimaId">
                    {{ ultimaId = conversa.historyId }}
                    <Button label="Conversa #1" severity="secondary" raised /><br><br>
                </div>
                
            </div>
            

        </div>
        <div class="menu-conversa">
            <div class="titulo-conversa">
                <h2 style="color: rgb(76, 76, 255)">CONVERSA</h2>
            </div>
            <Divider />
            <div class="box" v-for="(conversation, id) in conversationHistory" :key="id">
                <TextBox :name="conversation.name" :avatarImage="conversation.image" 
                    :message="conversation.text" :type="conversation.type"/>
            </div>
            
                <label for=""> Type here your message!</label> <br>
                <br> <br> 
                <InputText type="text"  v-model="dialog.text" />       
                <Button @click="sendMessage" label="Send"></Button>
                <hr>
                <!-- <div>
                    <h5>Bard: 😎</h5>
                    <p> {{ response }} </p>
                </div> -->
        </div>
         
    </div>
    
</template>

<style scoped>

    .menu-lateral{
        background-color: rgb(76, 76, 255);
        width: 250px; 
        height: 100vh;
        text-align: center;
    }

    .titulo{
        text-align: center; 
    }

    .menu-conversa{
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