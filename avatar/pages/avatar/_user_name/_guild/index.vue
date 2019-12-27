<template>
  <AvatarCard :user_name="$route.params.user_name" :guild="$route.params.guild" />
</template>

<script>
import AvatarCard from '~/components/AvatarCard.vue'

export default {
  components: {
    AvatarCard
  }
}
</script>
