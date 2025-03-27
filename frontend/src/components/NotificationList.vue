<template>
	<div class="position-fixed top-0 end-0 p-3" style="z-index: 1050">
		<TransitionGroup name="alert" tag="div">
			<div
				v-for="notification in notifications"
				:key="notification.id"
				:class="[
					'alert',
					bootstrapAlertClass(notification.type),
					'fade',
					'show',
				]"
				role="alert"
				@click="removeNotification(notification.id)"
			>
				{{ notification.message }}
			</div>
		</TransitionGroup>
	</div>
</template>

<script setup>
	import { useNotificationStore } from "../stores/notificationStore";
	import { storeToRefs } from "pinia";

	const notificationStore = useNotificationStore();
	const { notifications } = storeToRefs(notificationStore);
	const { removeNotification } = notificationStore;

	const bootstrapAlertClass = (type) => {
		switch (type) {
			case "error":
				return "alert-danger";
			case "warning":
				return "alert-warning";
			case "info":
				return "alert-info";
			case "success":
				return "alert-success";
			default:
				return "alert-secondary";
		}
	};
</script>

<style scoped>
	.alert-enter-active,
	.alert-leave-active {
		transition: opacity 0.3s;
	}
	.alert-enter-from,
	.alert-leave-to {
		opacity: 0;
	}
</style>
