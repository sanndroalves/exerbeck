<script setup>
const props = defineProps({
    avatarImage: { type: String },
    name: { type: String },
    message: { type: String },
    type: { type: String }
})

/* modo de comunicar props e css mais indicado quando não há tantas variações
const cardStyle = computed(()=> props.type === 'right' ? 
    {
        backColor: 'red',
        fontSize: '1.5rem',
        textColor: 'white'
    } 
: 
    {
        backColor: 'black',
        fontSize: '3.5rem',
        textColor: 'yellow'
    }    
)*/

const tipo = ref('')
switch(props.type){
    case 'A':
        tipo.value = 'left'
        break;
    case 'Q':
        tipo.value = 'right'
        break;
    case 'right':
        tipo.value = 'right'
        break;
}

console.log("T", tipo.value)
</script>

<template>
    <div class="text-box" :class="tipo === 'right' ? 'right-style' : 'left-style'">
        <Fieldset>
            <template #legend>
                <div class="flex align-items-center pl-2">
                    <Avatar :image="props.avatarImage" shape="circle" />
                    <span class="font-bold"> {{ props.name }}</span>
                </div>
            </template>
            <p class="m-0">
                {{ props.message }}
                <div v-if="props.type === 'right'">
                    <br>
                    <code style="font-size: 12px;">Digite "Oi" para ir para o início.</code>
                </div>
            </p>
        </Fieldset>
    </div>
</template>

<style scoped lang="scss">
/* modo de comunicar props e css mais indicado quando não há tantas variações
    .p-fieldset{
        background-color: v-bind(cardStyle.backColor);
        font-size: v-bind(cardStyle.fontSize);
        color: v-bind(cardStyle.textColor);
    }*/

.text-box {
    width: 700px;
    .p-fieldset {
        font-size: 1rem;
        color: black;       
    }
}

.right-style {
    .p-fieldset {
        background-color: fff;
        color: black;
    }
}

.left-style {
    .p-fieldset {
        background-color: rgb(76, 76, 255);
        color: white;
    }
}
</style>