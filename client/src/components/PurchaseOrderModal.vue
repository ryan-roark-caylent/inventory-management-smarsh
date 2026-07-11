<template>
  <div v-if="isOpen" class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-container">
      <div class="modal-header">
        <h2>{{ mode === 'create' ? 'Create Purchase Order' : 'Purchase Order Details' }}</h2>
        <button class="close-btn" @click="$emit('close')">&times;</button>
      </div>

      <div class="modal-body">
        <form v-if="mode === 'create'" @submit.prevent="submitForm">
          <div class="form-group">
            <label>Backlog Item</label>
            <input type="text" :value="backlogItem?.title" disabled />
          </div>

          <div class="form-group">
            <label>Supplier Name *</label>
            <input v-model="form.supplier_name" type="text" required />
          </div>

          <div class="form-group">
            <label>Quantity *</label>
            <input v-model.number="form.quantity" type="number" min="1" required />
          </div>

          <div class="form-group">
            <label>Unit Cost *</label>
            <input v-model.number="form.unit_cost" type="number" step="0.01" min="0" required />
          </div>

          <div class="form-group">
            <label>Expected Delivery Date *</label>
            <input v-model="form.expected_delivery_date" type="date" required />
          </div>

          <div class="form-group">
            <label>Notes</label>
            <textarea v-model="form.notes" rows="3"></textarea>
          </div>

          <div v-if="error" class="error-message">{{ error }}</div>

          <div class="form-actions">
            <button type="button" @click="$emit('close')">Cancel</button>
            <button type="submit" :disabled="submitting">
              {{ submitting ? 'Creating...' : 'Create PO' }}
            </button>
          </div>
        </form>

        <div v-else class="po-details">
          <p>Purchase order details view (extra credit).</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import { api } from '../api'

export default {
  name: 'PurchaseOrderModal',
  props: {
    isOpen: Boolean,
    backlogItem: Object,
    mode: {
      type: String,
      default: 'create'
    }
  },
  emits: ['close', 'po-created'],
  setup(props, { emit }) {
    const submitting = ref(false)
    const error = ref(null)
    const form = reactive({
      supplier_name: '',
      quantity: 1,
      unit_cost: 0,
      expected_delivery_date: '',
      notes: ''
    })

    const submitForm = async () => {
      if (!props.backlogItem) return
      submitting.value = true
      error.value = null
      try {
        const payload = {
          backlog_item_id: props.backlogItem.id,
          supplier_name: form.supplier_name,
          quantity: form.quantity,
          unit_cost: form.unit_cost,
          expected_delivery_date: form.expected_delivery_date,
          notes: form.notes || null
        }
        const result = await api.createPurchaseOrder(payload)
        emit('po-created', result)
      } catch (err) {
        error.value = err.response?.data?.detail || 'Failed to create purchase order'
      } finally {
        submitting.value = false
      }
    }

    return { form, submitting, error, submitForm }
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}
.modal-container {
  background: white;
  border-radius: 8px;
  padding: 24px;
  width: 500px;
  max-width: 90vw;
  max-height: 90vh;
  overflow-y: auto;
}
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}
.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
}
.form-group {
  margin-bottom: 16px;
}
.form-group label {
  display: block;
  margin-bottom: 4px;
  font-weight: 500;
}
.form-group input,
.form-group textarea {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
.error-message {
  color: red;
  margin-bottom: 12px;
}
.form-actions {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
}
.form-actions button {
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
}
</style>
