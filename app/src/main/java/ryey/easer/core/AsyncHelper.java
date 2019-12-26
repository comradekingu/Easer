/*
 * Copyright (c) 2016 - 2019 Rui Zhao <renyuneyun@gmail.com>
 *
 * This file is part of Easer.
 *
 * Easer is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * Easer is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with Easer.  If not, see <http://www.gnu.org/licenses/>.
 */

package ryey.easer.core;

import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.content.ServiceConnection;
import android.os.Bundle;
import android.os.Handler;
import android.os.IBinder;
import android.os.ParcelUuid;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.Callable;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

import ryey.easer.commons.local_skill.dynamics.DynamicsLink;

public final class AsyncHelper {

    public static class DelayedWhenSatisfied {

        private interface OnSatisfiedProcessQueue {
            void process();
        }

        protected AtomicBoolean satisfied = new AtomicBoolean(false);

        protected Lock lck_tasks = new ReentrantLock();
        protected List<Callable<Void>> tasksAfterConnect = new ArrayList<>();

        private OnSatisfiedProcessQueue onSatisfiedProcessQueue = new OnSatisfiedProcessQueue() {
            @Override
            public void process() {
                lck_tasks.lock();
                try {
                    for (int i = tasksAfterConnect.size() - 1; i >= 0; i--) {
                        Callable<Void> task = tasksAfterConnect.get(i);
                        try {
                            task.call();
                        } catch (Exception e) {
                            e.printStackTrace();
                        }
                        tasksAfterConnect.remove(i);
                    }
                } finally {
                    lck_tasks.unlock();
                }
            }
        };

        public void onSatisfied() {
            satisfied.set(true);
            onSatisfiedProcessQueue.process();
        }

        public void onUnsatisfied() {
            satisfied.set(false);
        }

        public void doAfter(Callable<Void> task) {
            lck_tasks.lock();
            try {
                if (satisfied.get()) {
                    try {
                        task.call();
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                } else {
                    tasksAfterConnect.add(task);
                }
            } finally {
                lck_tasks.unlock();
            }
        }
    }

    public static class DelayedServiceBinderJobs<B> extends DelayedWhenSatisfied {

        @Nullable
        protected B binder;

        public void onBind(B binder) {
            lck_tasks.lock();
            try {
                this.binder = binder;
                super.onSatisfied();
            } finally {
                lck_tasks.unlock();
            }
        }

        public void onUnbind() {
            lck_tasks.lock();
            try {
                super.onUnsatisfied();
                this.binder = null;
            } finally {
                lck_tasks.unlock();
            }
        }

        public void doAfter(Job<B> job) {
            doAfter(() -> {
                job.run(binder);
                return null;
            });
        }

        interface Job<B> {
            void run(B binder);
        }
    }

    public static class DelayedLoadProfileJobs extends DelayedServiceBinderJobs<ProfileLoaderService.PLSBinder> {

        private void doAfterSatisfied(TaskSpec taskSpec) {
            doAfter(() -> {
                if (taskSpec.scriptName == null) {
                    binder.triggerProfile(taskSpec.profileName);
                } else {
                    binder.triggerProfile(taskSpec.profileName, taskSpec.scriptName,
                            taskSpec.dynamicsProperties, taskSpec.dynamicsLink);
                }
                return null;
            });
        }

        public void triggerProfile(String profileName) {
            doAfterSatisfied(new TaskSpec(profileName, null, null, null));
        }
        public void triggerProfile(String profileName, String scriptName,
                                   Bundle dynamicsProperties, DynamicsLink dynamicsLink) {
            doAfterSatisfied(new TaskSpec(profileName, scriptName, dynamicsProperties, dynamicsLink));
        }

        private static class TaskSpec {
            @NonNull public final String profileName;
            @Nullable public final String scriptName;
            @Nullable public final Bundle dynamicsProperties;
            @Nullable public final DynamicsLink dynamicsLink;

            public TaskSpec(@NonNull String profileName, @Nullable String scriptName, @Nullable Bundle dynamicsProperties, @Nullable DynamicsLink dynamicsLink) {
                this.profileName = profileName;
                this.scriptName = scriptName;
                this.dynamicsProperties = dynamicsProperties;
                this.dynamicsLink = dynamicsLink;
            }
        }
    }

    public static class DelayedLoadProfileJobsWrapper {
        private final DelayedLoadProfileJobs jobLoadProfile = new DelayedLoadProfileJobs();
        private final ServiceConnection connection;

        public DelayedLoadProfileJobsWrapper() {
            connection = new ServiceConnection() {
                @Override
                public void onServiceConnected(ComponentName name, IBinder service) {
                    jobLoadProfile.onBind((ProfileLoaderService.PLSBinder) service);
                }

                @Override
                public void onServiceDisconnected(ComponentName name) {
                    jobLoadProfile.onUnbind();
                }
            };
        }

        public DelayedLoadProfileJobsWrapper(ServiceConnection connection) {
            this.connection = connection;
        }

        public void bindService(Context context) {
            context.bindService(new Intent(context, ProfileLoaderService.class), connection, Context.BIND_AUTO_CREATE);
        }

        public void unbindService(Context context) {
            context.unbindService(connection);
        }

        public void triggerProfile(String profileName) {
            jobLoadProfile.triggerProfile(profileName);
        }

        public void triggerProfile(String profileName, String scriptName, Bundle dynamicsProperties, DynamicsLink dynamicsLink) {
            jobLoadProfile.triggerProfile(profileName, scriptName, dynamicsProperties, dynamicsLink);
        }
    }

    public static class CallbackStore<T>  {
        protected Lock lckCallbackMap = new ReentrantLock();
        protected final Map<ParcelUuid, T> callbackMap;

        public CallbackStore(Map<ParcelUuid, T> callbackMap) {
            this.callbackMap = callbackMap;
        }

        public ParcelUuid putCallback(T callback) {
            ParcelUuid uuid = new ParcelUuid(UUID.randomUUID());
            putCallback(uuid, callback);
            return uuid;
        }

        public void putCallback(UUID uuid, T callback) {
            putCallback(new ParcelUuid(uuid), callback);
        }

        public void putCallback(ParcelUuid uuid, T callback) {
            lckCallbackMap.lock();
            try {
                callbackMap.put(uuid, callback);
            } finally {
                lckCallbackMap.unlock();
            }
        }

        @Nullable
        public T extractCallBack(ParcelUuid uuid) {
            lckCallbackMap.lock();
            try {
                T callback = callbackMap.get(uuid);
                //noinspection VariableNotUsedInsideIf
                if (callback != null)
                    callbackMap.remove(uuid);
                return callback;
            } finally {
                lckCallbackMap.unlock();
            }
        }
    }

    public abstract static class TimedCallbackStore<T> extends CallbackStore<T> {

        public final long defaultTimeout;

        protected Handler handler = new Handler();

        public TimedCallbackStore(Map<ParcelUuid, T> callbackMap, long defaultTimeout) {
            super(callbackMap);
            this.defaultTimeout = defaultTimeout;
        }

        public void putCallback(ParcelUuid uuid, T callback) {
            putCallback(uuid, callback, defaultTimeout);
        }

        public void putCallback(ParcelUuid uuid, T callback, long milliseconds) {
            lckCallbackMap.lock();
            try {
                callbackMap.put(uuid, callback);
                handler.postDelayed(() -> _timeout(uuid), milliseconds);
            } finally {
                lckCallbackMap.unlock();
            }
        }

        private void _timeout(ParcelUuid uuid) {
            T callback = extractCallBack(uuid);
            if (callback != null) {
                onTimeout(uuid, callback);
            }
        }

        protected abstract void onTimeout(ParcelUuid uuid, T callback);

    }
}
