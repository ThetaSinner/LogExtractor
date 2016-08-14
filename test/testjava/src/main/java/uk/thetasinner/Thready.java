package uk.thetasinner;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.atomic.AtomicInteger;

public class Thready {

  private static Runnable task;

  public static void main(String[] args) {

    final AtomicInteger i = new AtomicInteger(0);

    ExecutorService executorService = Executors.newFixedThreadPool(3);

    task = new Runnable() {
      public void run() {
        System.out.println(i.incrementAndGet());
      }
    };

    for (int k = 0; k < 40; k++)
    {
      executorService.submit(task);
    }
  }
}
