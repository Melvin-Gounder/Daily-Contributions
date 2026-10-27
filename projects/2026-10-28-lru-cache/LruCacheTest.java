public final class LruCacheTest {
    private static int passed = 0;

    public static void main(String[] args) {
        rejectsInvalidCapacity();
        returnsInsertedValue();
        evictsLeastRecentlyUsed();
        getChangesRecency();
        updatingKeyDoesNotGrowCache();
        missingKeyReturnsEmpty();
        System.out.println("All " + passed + " LRU cache tests passed.");
    }

    private static void rejectsInvalidCapacity() {
        boolean thrown = false;
        try { new LruCache<String, Integer>(0); }
        catch (IllegalArgumentException expected) { thrown = true; }
        check(thrown, "zero capacity should be rejected");
    }

    private static void returnsInsertedValue() {
        LruCache<String, Integer> cache = new LruCache<>(2);
        cache.put("x", 7);
        check(cache.get("x").orElseThrow() == 7, "inserted value should be returned");
    }

    private static void evictsLeastRecentlyUsed() {
        LruCache<String, Integer> cache = new LruCache<>(2);
        cache.put("a", 1); cache.put("b", 2); cache.put("c", 3);
        check(!cache.containsKey("a") && cache.containsKey("b") && cache.containsKey("c"), "oldest key should be evicted");
    }

    private static void getChangesRecency() {
        LruCache<String, Integer> cache = new LruCache<>(2);
        cache.put("a", 1); cache.put("b", 2); cache.get("a"); cache.put("c", 3);
        check(cache.containsKey("a") && !cache.containsKey("b"), "get should promote a key before eviction");
    }

    private static void updatingKeyDoesNotGrowCache() {
        LruCache<String, Integer> cache = new LruCache<>(2);
        cache.put("a", 1); cache.put("a", 99);
        check(cache.size() == 1 && cache.get("a").orElseThrow() == 99, "update should replace value without adding an entry");
    }

    private static void missingKeyReturnsEmpty() {
        LruCache<String, Integer> cache = new LruCache<>(1);
        check(cache.get("missing").isEmpty(), "missing key should return Optional.empty");
    }

    private static void check(boolean condition, String message) {
        if (!condition) throw new AssertionError(message);
        passed++;
    }
}
