<template>
  <div id="app" v-if="!isFetching">
    <v-app id="inspire">
      <v-card max-width="344" class="mx-auto">
        <v-list-item>
          <v-list-item-avatar color="grey">
            <v-avatar>
              <img :src="avatar_image_url" alt="Raul Lanuza" />
            </v-avatar>
          </v-list-item-avatar>
          <v-list-item-content>
            <v-list-item-title class="headline">{{user_name}}</v-list-item-title>
            <v-list-item-subtitle>{{guild}}</v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>

        <v-img :src="level_image_url" height="194" contain="true"></v-img>

        <v-card-text>
          Exp: {{exp}}
          <v-spacer />
          Level: {{level}}
        </v-card-text>
      </v-card>
    </v-app>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AvatarCard',
  props: [
    'user_name',
    'guild',
    'avatar_image_url',
    'level_image_url',
    'exp',
    'level'
  ],

  data: () => ({})
}
</script>
