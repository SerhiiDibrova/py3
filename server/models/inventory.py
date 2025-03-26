

package server.models;

public class Inventory {
    private int inventory_id;
    private int branch_id;
    private int book_id;
    private int available_copies;
    private int damaged_copies;
    private String status;

    public Inventory(int inventory_id, int branch_id, int book_id, int available_copies, int damaged_copies, String status) {
        this.inventory_id = inventory_id;
        this.branch_id = branch_id;
        this.book_id = book_id;
        this.available_copies = available_copies;
        this.damaged_copies = damaged_copies;
        this.status = status;
    }

    public int getInventory_id() {
        return inventory_id;
    }

    public void setInventory_id(int inventory_id) {
        this.inventory_id = inventory_id;
    }

    public int getBranch_id() {
        return branch_id;
    }

    public void setBranch_id(int branch_id) {
        this.branch_id = branch_id;
    }

    public int getBook_id() {
        return book_id;
    }

    public void setBook_id(int book_id) {
        this.book_id = book_id;
    }

    public int getAvailable_copies() {
        return available_copies;
    }

    public void setAvailable_copies(int available_copies) {
        this.available_copies = available_copies;
    }

    public int getDamaged_copies() {
        return damaged_copies;
    }

    public void setDamaged_copies(int damaged_copies) {
        this.damaged_copies = damaged_copies;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }
}