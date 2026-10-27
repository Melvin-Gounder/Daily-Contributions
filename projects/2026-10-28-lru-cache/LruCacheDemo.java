public final class LruCacheDemo {
    public static void main(String[] args) {
        LruCache<String, Integer> cache = new LruCache<>(3);

        cache.put("A", 10);
        cache.put("B", 20);
        cache.put("C", 30);
        System.out.println("After A, B, C: " + cache.keysMostRecentFirst());

        System.out.println("Read A = " + cache.get("A").orElseThrow());
        System.out.println("After reading A: " + cache.keysMostRecentFirst());

        cache.put("D", 40);
        System.out.println("After adding D: " + cache.keysMostRecentFirst());
        System.out.println("B was evicted: " + !cache.containsKey("B"));
    }
}
