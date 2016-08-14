package uk.thetasinner;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;
import java.math.BigInteger;
import java.security.SecureRandom;

/**
 * Created by ThetaSinner on 04/03/2016.
 * <p>
 * Write either a nice string or a dirty exception to file.
 */
public class LogWriter {
  private static final Logger LOG = LoggerFactory.getLogger(LogWriter.class);

  public static void main(String[] args) throws IOException, InterruptedException {
    while (true) {
      new LogWriter().dumpCrap(20);
    }
  }

  public void dumpCrap(int countDown) throws InterruptedException, IOException {
    if (countDown <= 0) {
      return;
    }

    Thread.sleep(1000);

    if ((int) Math.floor(Math.random() * 10) % 3 == 0) {
      try {
        LogWriter lw = null;
        lw.dumpCrap(0);
      } catch (final NullPointerException npe) {
        LOG.error("an exception", npe);
      }
    }
    else {
      LOG.debug(new BigInteger(130, new SecureRandom()).toString());
    }

    dumpCrap(countDown - 1);
  }
}
