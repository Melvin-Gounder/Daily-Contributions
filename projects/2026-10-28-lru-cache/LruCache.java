import java.util.HashMap;
import java.util.Map;
import java.util.Optional;

/**
 * Fixed-capacity Least Recently Used cache.
 *
 * HashMap: key -> linked-list node for average O(1) lookup.
 * Doubly linked list: O(1) promotion and eviction once a node is known.
 */
public final class LruCache<K, V> {
    private final int capacity;
    private final Map<K, Node<K, V>> index = new HashMap<>();
    private final Node<K, V> head = new Node<>(null, null);
    private final Node<K, V> tail = new Node<>(null, null);

    public LruCache(int capacity) {
        if (capacity <= 0) {
            throw new IllegalArgumentException("capacity must be greater than zero");
        }
        this.capacity = capacity;
        head.next = tail;
        tail.previous = head;
    }

    public Optional<V> get(K key) {
        Node<K, V> node = index.get(key);
        if (node == null) {
            return Optional.empty();
        }
        moveToFront(node);
        return Optional.ofNullable(node.value);
    }

    public void put(K key, V value) {
        Node<K, V> existing = index.get(key);
        if (existing != null) {
            existing.value = value;
            moveToFront(existing);
            return;
        }

        Node<K, V> node = new Node<>(key, value);
        index.put(key, node);
        addAfterHead(node);

        if (index.size() > capacity) {
            evictLeastRecentlyUsed();
        }
    }

    public boolean containsKey(K key) {
        return index.containsKey(key);
    }

    public int size() {
        return index.size();
    }

    public String keysMostRecentFirst() {
        StringBuilder result = new StringBuilder();
        Node<K, V> current = head.next;
        while (current != tail) {
            if (result.length() > 0) result.append(" -> ");
            result.append(current.key);
            current = current.next;
        }
        return result.toString();
    }

    private void moveToFront(Node<K, V> node) {
        unlink(node);
        addAfterHead(node);
    }

    private void evictLeastRecentlyUsed() {
        Node<K, V> victim = tail.previous;
        if (victim == head) return;
        unlink(victim);
        index.remove(victim.key);
    }

    private void addAfterHead(Node<K, V> node) {
        node.previous = head;
        node.next = head.next;
        head.next.previous = node;
        head.next = node;
    }

    private void unlink(Node<K, V> node) {
        node.previous.next = node.next;
        node.next.previous = node.previous;
    }

    private static final class Node<K, V> {
        private final K key;
        private V value;
        private Node<K, V> previous;
        private Node<K, V> next;

        private Node(K key, V value) {
            this.key = key;
            this.value = value;
        }
    }
}
