<template>
  <AvatarCard
    :user_name="$route.params.user_name"
    :guild="$route.params.guild"
    :avatar_image_url="$route.params.avatar_url"
    :level_image_url="$route.params.level_url"
    :exp="$route.params.exp"
    :level="$route.params.level"
  />
</template>

<script>
import AvatarCard from '~/components/AvatarCard.vue'

export default {
  components: {
    AvatarCard
  }
}
</script>
